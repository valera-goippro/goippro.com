<?php if (!defined('ABSPATH')) { exit; } ?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
  <meta charset="<?php bloginfo('charset'); ?>">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<?php if (!is_page_template('page-goip-technology.php') && !is_page_template('page-home.php')): ?>
<!-- Language switcher for React pages - will be moved to header by JavaScript -->
<div id="gtranslate-widget" style="display: none;">
  <?php echo do_shortcode('[gtranslate]'); ?>
</div>
<div id="root">
<?php endif; ?>


