<?php
// Prevent direct access
if (!defined('ABSPATH')) { exit; }

// Enqueue production assets via Vite manifest
function soft24_enqueue_assets() {
    // Don't load React assets on GoIP Technology page
    if (is_page_template('page-goip-technology.php')) {
        return;
    }
    
    $theme_dir = get_stylesheet_directory();
    $theme_uri = get_stylesheet_directory_uri();

    // Read manifest (support .vite/manifest.json and manifest.json)
    $manifest_path = $theme_dir . '/dist/.vite/manifest.json';
    if (!file_exists($manifest_path)) {
        $manifest_path = $theme_dir . '/dist/manifest.json';
    }
    if (!file_exists($manifest_path)) { return; }

    $manifest = json_decode(file_get_contents($manifest_path), true);
    if (!is_array($manifest)) { return; }

    $entry = isset($manifest['src/main.tsx']) ? $manifest['src/main.tsx'] : null;
    if (!$entry) { return; }

    // CSS files
    if (!empty($entry['css']) && is_array($entry['css'])) {
        foreach ($entry['css'] as $idx => $css_rel_path) {
            wp_enqueue_style('soft24-style-' . $idx, $theme_uri . '/dist/' . ltrim($css_rel_path, '/'), [], '1.0.' . time());
        }
    }

    // JS file
    if (!empty($entry['file'])) {
        wp_enqueue_script('soft24-main', $theme_uri . '/dist/' . ltrim($entry['file'], '/'), [], '1.0.' . time(), true);
        add_filter('script_loader_tag', function ($tag, $handle, $src) {
            if ($handle === 'soft24-main') {
                return str_replace('<script ', '<script type="module" ', $tag);
            }
            return $tag;
        }, 10, 3);
    }
}
add_action('wp_enqueue_scripts', 'soft24_enqueue_assets');

// Theme supports
add_action('after_setup_theme', function () {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    
    // Add featured image sizes for blog
    add_image_size('blog-thumbnail', 400, 300, true);
    add_image_size('blog-hero', 1200, 600, true);
});

// Register custom page templates
function soft24_page_templates($templates) {
    $templates['page-goip-technology.php'] = 'GoIP Technology';
    return $templates;
}
add_filter('theme_page_templates', 'soft24_page_templates');

// Flush rewrite rules on theme activation
function soft24_flush_rewrite_rules() {
    flush_rewrite_rules();
}
add_action('after_switch_theme', 'soft24_flush_rewrite_rules');

// Expose WordPress data to React app
add_action('wp_head', function () {
    $base = get_stylesheet_directory_uri();
    $assets_base = trailingslashit($base) . 'dist';
    $api_data = array(
        'baseUrl' => $base,
        'assetsBaseUrl' => $assets_base,
        'apiUrl' => home_url('/wp-json/wp/v2'),
        'nonce' => wp_create_nonce('wp_rest'),
        'siteUrl' => home_url()
    );
    echo '<script>window.SOFT24_THEME = ' . json_encode($api_data) . ';</script>' . "\n";
    
    // Add script to move gtranslate to header after React loads
    echo '<script>
        // Wait for React to load and render
        function moveGtranslateToHeader() {
            const placeholder = document.getElementById("gtranslate-header-placeholder");
            const gtranslateWidget = document.getElementById("gtranslate-widget");
            
            if (placeholder && gtranslateWidget && gtranslateWidget.children.length > 0) {
                // Use jQuery if available (more reliable)
                if (typeof jQuery !== "undefined") {
                    jQuery(gtranslateWidget).children().appendTo(placeholder);
                    jQuery(placeholder).show();
                    jQuery(gtranslateWidget).hide();
                    console.log("GTranslate moved to header with jQuery");
                } else {
                    // Fallback: Move DOM elements manually
                    const children = Array.from(gtranslateWidget.children);
                    children.forEach(child => {
                        placeholder.appendChild(child);
                    });
                    placeholder.style.display = "block";
                    gtranslateWidget.style.display = "none";
                    console.log("GTranslate moved to header with vanilla JS");
                }
                
                // Re-initialize gtranslate if needed
                if (typeof doGTranslate !== "undefined") {
                    console.log("GTranslate function available");
                }
            } else {
                // Try again after 200ms if React hasn\'t loaded yet or gtranslate not ready
                setTimeout(moveGtranslateToHeader, 200);
            }
        }
        
        // Multiple attempts with different timing
        document.addEventListener("DOMContentLoaded", function() {
            setTimeout(moveGtranslateToHeader, 800);
            setTimeout(moveGtranslateToHeader, 1500); // Second attempt
        });
        
        window.addEventListener("load", function() {
            setTimeout(moveGtranslateToHeader, 300);
        });
    </script>' . "\n";
});

// Enable REST API for posts with featured images
add_action('rest_api_init', function () {
    // Add featured image URLs to REST API response
    register_rest_field('post', 'featured_image_urls', array(
        'get_callback' => function ($post) {
            $image_id = get_post_thumbnail_id($post['id']);
            if (!$image_id) return null;
            
            return array(
                'thumbnail' => wp_get_attachment_image_url($image_id, 'blog-thumbnail'),
                'full' => wp_get_attachment_image_url($image_id, 'blog-hero')
            );
        },
        'schema' => null,
    ));
    
    // Add formatted date
    register_rest_field('post', 'formatted_date', array(
        'get_callback' => function ($post) {
            return get_the_date('', $post['id']);
        },
        'schema' => null,
    ));
    
    // Add author name
    register_rest_field('post', 'author_name', array(
        'get_callback' => function ($post) {
            return get_the_author_meta('display_name', $post['author']);
        },
        'schema' => null,
    ));
});

// Long-term caching for theme assets and images (1 year)
add_action('send_headers', function () {
    $uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
    // Cache theme dist assets (hashed filenames)
    if (strpos($uri, '/wp-content/themes/soft24/dist/') !== false) {
        header('Cache-Control: public, max-age=31536000, immutable');
        return;
    }
    // Cache images from any location
    if (preg_match('/\.(?:png|jpe?g|gif|svg|webp|ico)$/i', $uri)) {
        header('Cache-Control: public, max-age=31536000, immutable');
    }
});

add_filter('wpcf7_autop_or_not', '__return_false');
add_filter('wpcf7_form_elements', function($content) {
  $content = str_replace('<span', '<div', $content);
  $content = str_replace('</span', '</div', $content);
  return $content;
});
