<?php
/**
 * Plugin Name:       Hans Larsen — ny hjemmeside
 * Description:       Viser den nye hjemmeside for Malerfirmaet Hans Larsen i stedet for WordPress-temaet. WordPress, temaet og indholdet bliver liggende urørt — deaktivér pluginet, så er den gamle side tilbage med det samme.
 * Version:           1.0.0
 * Requires at least: 5.5
 * Requires PHP:      7.0
 * License:           GPL-2.0-or-later
 * Text Domain:       hanslarsen-site
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'HLS_VERSION', '1.0.0' );
define( 'HLS_SITE_DIR', __DIR__ . '/site/' );

/**
 * The only addresses that serve a page. Everything else is a redirect or the
 * 404 page -- no part of the request ever reaches the file system.
 */
function hls_routes() {
	return array(
		''                  => 'index.html',
		'om-os'             => 'om-os/index.html',
		'haandverksgruppen' => 'haandverksgruppen/index.html',
		'groen-omstilling'  => 'groen-omstilling/index.html',
		'arbejdsmiljoe'     => 'arbejdsmiljoe/index.html',
		'kontakt'           => 'kontakt/index.html',
	);
}

/**
 * Request path relative to the WordPress home, without surrounding slashes,
 * plus whether it ended in a slash.
 *
 * @return array{0:string,1:bool}
 */
function hls_request_path() {
	$uri  = isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '/';
	$path = rawurldecode( (string) wp_parse_url( $uri, PHP_URL_PATH ) );
	$home = (string) wp_parse_url( home_url( '/' ), PHP_URL_PATH );

	if ( '' !== $home && '/' !== $home && 0 === strpos( $path, $home ) ) {
		$path = '/' . substr( $path, strlen( $home ) );
	}
	$trailing = ( '' === $path || '/' === substr( $path, -1 ) );
	return array( trim( $path, '/' ), $trailing );
}

function hls_query_suffix() {
	$q = isset( $_SERVER['QUERY_STRING'] ) ? (string) $_SERVER['QUERY_STRING'] : '';
	return '' === $q ? '' : '?' . $q;
}

function hls_is_head() {
	return isset( $_SERVER['REQUEST_METHOD'] ) && 'HEAD' === strtoupper( (string) $_SERVER['REQUEST_METHOD'] );
}

function hls_redirect( $to ) {
	wp_redirect( $to, 301, 'Hans Larsen' );
	exit;
}

/**
 * Send one of the site's HTML files with its URL placeholders filled in.
 */
function hls_render( $file, $status ) {
	$full = HLS_SITE_DIR . $file;
	if ( ! is_readable( $full ) ) {
		return;
	}
	$html = (string) file_get_contents( $full );
	$html = str_replace(
		array( '{{HLS_HOME}}', '{{HLS_ASSETS}}' ),
		array( esc_url( home_url( '/' ) ), esc_url( plugins_url( 'site/', __FILE__ ) ) ),
		$html
	);

	status_header( $status );
	header( 'Content-Type: text/html; charset=UTF-8' );
	if ( 404 === $status ) {
		nocache_headers();
	}
	if ( ! hls_is_head() ) {
		echo $html; // phpcs:ignore WordPress.Security.EscapeOutput -- static file shipped with the plugin.
	}
	exit;
}

function hls_send_file( $file, $content_type ) {
	$full = HLS_SITE_DIR . $file;
	if ( ! is_readable( $full ) ) {
		return;
	}
	status_header( 200 );
	header( 'Content-Type: ' . $content_type );
	if ( ! hls_is_head() ) {
		readfile( $full ); // phpcs:ignore WordPress.WP_Filesystem
	}
	exit;
}

/**
 * Admins can still look at the old theme: add ?hls-gammel to any address.
 */
function hls_admin_wants_old_site() {
	return isset( $_GET['hls-gammel'] ) && is_user_logged_in() && current_user_can( 'manage_options' ); // phpcs:ignore WordPress.Security.NonceVerification
}

/**
 * Runs on template_redirect at priority 0: after WordPress has parsed the
 * request, before its canonical and sitemap redirects (priority 10) and
 * before the theme loads. Admin, login, REST, AJAX, cron and XML-RPC never
 * reach this hook, so wp-admin keeps working and the plugin can always be
 * switched off from there.
 */
function hls_route() {
	if ( is_admin() || wp_doing_ajax() || is_customize_preview() || hls_admin_wants_old_site() ) {
		return;
	}
	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return;
	}

	list( $path, $trailing ) = hls_request_path();
	$routes = hls_routes();
	$home   = home_url( '/' );

	if ( isset( $routes[ $path ] ) ) {
		if ( '' !== $path && ! $trailing ) {
			hls_redirect( $home . $path . '/' . hls_query_suffix() );
		}
		hls_render( $routes[ $path ], 200 );
	}

	if ( 'robots.txt' === $path ) {
		hls_send_file( 'robots.txt', 'text/plain; charset=UTF-8' );
	}
	if ( 'sitemap.xml' === $path ) {
		hls_send_file( 'sitemap.xml', 'application/xml; charset=UTF-8' );
	}

	// WordPress addresses that no longer exist.
	if ( preg_match( '#^wp-sitemap.*\.xml$#', $path ) ) {
		hls_redirect( $home . 'sitemap.xml' );
	}
	if ( 'hello-world' === $path
		|| preg_match( '#^(category|author|tag)(/|$)#', $path )
		|| preg_match( '#^(comments/)?feed$#', $path ) ) {
		hls_redirect( $home );
	}

	// Preview links shared before launch: /om-os.html -> /om-os/
	if ( preg_match( '#^([a-z-]+)\.html$#', $path, $m ) && isset( $routes[ $m[1] ] ) && '' !== $m[1] ) {
		hls_redirect( $home . $m[1] . '/' );
	}

	hls_render( '404.html', 404 );
}
add_action( 'template_redirect', 'hls_route', 0 );

/*
 * WordPress' own sitemaps redirect /sitemap.xml to /wp-sitemap.xml from
 * pre_handle_404 -- before template_redirect ever runs -- and hls_route sends
 * /wp-sitemap.xml back to /sitemap.xml: a redirect loop on the one file
 * Google fetches. The site has its own sitemap, so switch the core one off.
 * The filter is read on `init`, after plugins have loaded.
 */
add_filter( 'wp_sitemaps_enabled', '__return_false' );

/**
 * Empty every page cache we know of, so switching the plugin on or off is
 * visible immediately instead of when a cached copy expires.
 */
function hls_purge_caches() {
	do_action( 'litespeed_purge_all' );
	if ( function_exists( 'rocket_clean_domain' ) ) {
		rocket_clean_domain();
	}
	if ( function_exists( 'w3tc_flush_all' ) ) {
		w3tc_flush_all();
	}
	if ( function_exists( 'wp_cache_clear_cache' ) ) {
		wp_cache_clear_cache();
	}
	if ( function_exists( 'wp_cache_flush' ) ) {
		wp_cache_flush();
	}
}
register_activation_hook( __FILE__, 'hls_purge_caches' );
register_deactivation_hook( __FILE__, 'hls_purge_caches' );

/**
 * Links on the plugin row.
 */
function hls_action_links( $links ) {
	$links[] = '<a href="' . esc_url( home_url( '/' ) ) . '" target="_blank">Se den nye side</a>';
	$links[] = '<a href="' . esc_url( add_query_arg( 'hls-gammel', '1', home_url( '/' ) ) ) . '" target="_blank">Se den gamle side</a>';
	return $links;
}
add_filter( 'plugin_action_links_' . plugin_basename( __FILE__ ), 'hls_action_links' );
