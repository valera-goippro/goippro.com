<?php
/**
 * Template Name: GoIP Technology
 * Template Post Type: page
 */

if (!defined('ABSPATH')) { exit; }
get_header(); 
?>

<style>
/* Tailwind-inspired styles matching main site */
.container-tight { max-width: 80rem; margin: 0 auto; padding: 0 1rem; }
@media (min-width: 640px) { .container-tight { padding: 0 1.5rem; } }
@media (min-width: 1024px) { .container-tight { padding: 0 2rem; } }

/* Hide auth buttons on mobile devices */
@media (max-width: 768px) {
  .mobile-hide-auth {
      display: none !important;
  }
}

/* Ensure mobile menu button is hidden on desktop */
@media (min-width: 640px) {
  #mobile-menu-btn, #mobile-menu {
      display: none !important;
  }
}

/* Icon styles */
.icon-gradient-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.icon-gradient-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.icon-gradient-3 { background: linear-gradient(135deg, #10b981 0%, #059669 100%); }
.icon-gradient-4 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
.icon-gradient-5 { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); }
.icon-gradient-6 { background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%); }

/* Modal styles */
.fixed { position: fixed; }
.inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
.z-50 { z-index: 50; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.absolute { position: absolute; }
.bg-black\/60 { background-color: rgba(0, 0, 0, 0.6); }
.backdrop-blur-sm { backdrop-filter: blur(4px); }
.relative { position: relative; }
.bg-white { background-color: white; }
.rounded-3xl { border-radius: 1.5rem; }
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
.max-w-md { max-width: 28rem; }
.w-full { width: 100%; }
.mx-4 { margin-left: 1rem; margin-right: 1rem; }
.overflow-hidden { overflow: hidden; }
.bg-gradient-to-r { background-image: linear-gradient(to right, #9333ea, #db2777, #ea580c); }
.p-6 { padding: 1.5rem; }
.text-white { color: white; }
.text-center { text-align: center; }
.w-16 { width: 4rem; }
.h-16 { height: 4rem; }
.bg-white\/20 { background-color: rgba(255, 255, 255, 0.2); }
.rounded-full { border-radius: 9999px; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mb-4 { margin-bottom: 1rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.font-bold { font-weight: 700; }
.mb-2 { margin-bottom: 0.5rem; }
.text-white\/90 { color: rgba(255, 255, 255, 0.9); }
.mb-6 { margin-bottom: 1.5rem; }
.block { display: block; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.font-medium { font-weight: 500; }
.text-gray-700 { color: #374151; }
.pl-12 { padding-left: 3rem; }
.pr-4 { padding-right: 1rem; }
.py-4 { padding-top: 1rem; padding-bottom: 1rem; }
.border { border-width: 1px; }
.border-gray-200 { border-color: #e5e7eb; }
.rounded-xl { border-radius: 0.75rem; }
.focus\:ring-2:focus { box-shadow: 0 0 0 2px rgb(147 51 234 / 0.5); }
.focus\:ring-purple-500:focus { box-shadow: 0 0 0 2px rgb(147 51 234 / 0.5); }
.focus\:border-transparent:focus { border-color: transparent; }
.transition-all { transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.hover\:shadow-lg:hover { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1); }
.transform { transform: translate(0, 0) rotate(0) skew(0, 0) scaleX(1) scaleY(1); }
.hover\:scale-105:hover { transform: scale(1.05); }
.duration-200 { transition-duration: 200ms; }
.gap-2 { gap: 0.5rem; }
.mt-6 { margin-top: 1.5rem; }
.space-y-3 > * + * { margin-top: 0.75rem; }
.text-purple-600 { color: #9333ea; }
.hover\:text-purple-700:hover { color: #7c3aed; }
.space-x-4 > * + * { margin-left: 1rem; }
.text-gray-500 { color: #6b7280; }
.hover\:text-purple-600:hover { color: #9333ea; }
.transition-colors { transition-property: color, background-color, border-color, text-decoration-color, fill, stroke; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms;    background: none;  border: none; }

/* Additional modal styles for full compatibility */
.btn { display: inline-flex; align-items: center; justify-content: center; border-radius: 1rem; font-weight: 600; transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 0.3s; }
.btn:focus-visible { outline: 2px solid transparent; outline-offset: 2px; box-shadow: 0 0 0 2px rgb(23 23 23 / 0.5); }
.btn:disabled { cursor: not-allowed; opacity: 0.5; }
.btn-primary { background-color: rgb(23 23 23); color: rgb(255 255 255); box-shadow: 0 8px 30px rgba(0,0,0,.12); display: inline-flex; align-items: center; justify-content: center; border-radius: 1rem; font-weight: 600; transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 0.3s; }
.btn-primary:hover { background-color: rgb(38 38 38); box-shadow: 0 10px 40px rgba(0,0,0,.2); }
.btn-primary:active { transform: scale(0.95); }

.input-field { width: 100%; border-radius: 1rem; border-width: 1px; border-color: rgb(212 212 212); background-color: rgba(255, 255, 255, 0.9); padding: 0.75rem 1rem; color: rgb(23 23 23); backdrop-filter: blur(4px); transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 0.2s; }
.input-field::-moz-placeholder { color: rgb(115 115 115); }
.input-field::placeholder { color: rgb(115 115 115); }
.input-field:focus { border-color: rgb(115 115 115); background-color: rgb(255 255 255); outline: 2px solid transparent; outline-offset: 2px; box-shadow: 0 0 0 2px rgb(229 229 229 / 0.5); }

/* Modal animation and transitions */
.animate-in { animation: animate-in 0.5s ease-out; }
@keyframes animate-in { 0% { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Close button styles */
.close-btn { position: absolute; top: 1rem; right: 1rem; width: 2rem; height: 2rem; border-radius: 50%; background-color: rgba(255, 255, 255, 0.1); color: white; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; border: none; }
.close-btn:hover { background-color: rgba(255, 255, 255, 0.2); transform: scale(1.1); }

/* Form validation styles */
.error-message { color: #ef4444; font-size: 0.875rem; margin-top: 0.5rem; display: none; }
.error-message.show { display: block; }

/* Tab switching styles */
.tab-button { background: none; border: none; color: #6b7280; font-size: 0.875rem; font-weight: 500; cursor: pointer; padding: 0.5rem 1rem; border-radius: 0.5rem; transition: all 0.2s; }
.tab-button.active { color: #9333ea; background-color: rgba(147, 51, 234, 0.1); }
.tab-button:hover { color: #9333ea; background-color: rgba(147, 51, 234, 0.05); }

/* Social login button styles */
.social-btn { display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: 0.75rem; background-color: white; color: #374151; font-size: 0.875rem; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.social-btn:hover { background-color: #f9fafb; border-color: #d1d5db; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
.social-btn img { width: 1.25rem; height: 1.25rem; }

/* Divider styles */
.divider { display: flex; align-items: center; margin: 1.5rem 0; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background-color: #e5e7eb; }
.divider span { padding: 0 1rem; color: #6b7280; font-size: 0.875rem; }

/* Additional utility classes */
.space-y-3 > * + * { margin-top: 0.75rem; }
.space-x-4 > * + * { margin-left: 1rem; }
.relative { position: relative; }
.left-3 { left: 0.75rem; }
.top-1\/2 { top: 50%; }
.transform { transform: translate(0, 0) rotate(0) skew(0, 0) scaleX(1) scaleY(1); }
.-translate-y-1\/2 { transform: translate(0, -50%); }
.text-gray-400 { color: #9ca3af; }
.text-gray-300 { color: #d1d5db; }
.hover\:text-purple-700:hover { color: #7c3aed; }
.cursor-pointer { cursor: pointer; }
.border-none { border: none; }

.feature-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.feature-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Arial, sans-serif;
  background-color: #fafafa;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(59, 130, 246, 0.04) 0%, transparent 50%),
    radial-gradient(circle at 75% 75%, rgba(168, 85, 247, 0.04) 0%, transparent 50%);
  color: #171717;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Header Navigation */
.nav-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding-top: 0.75rem;
}

.nav-container {
  margin: 0 auto;
  max-width: 80rem;
  padding: 0 1rem;
}

.nav-bar {
  border-radius: 1rem;
  border: 1px solid rgba(229, 229, 229, 0.6);
  background-color: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 1rem;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
}

.nav-logo-icon {
  height: 2.25rem;
  width: 2.25rem;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-logo-text {
  font-size: 1rem;
  font-weight: 700;
  color: #171717;
}

.nav-menu {
  display: none;
  align-items: center;
  gap: 0.25rem;
}

@media (min-width: 640px) {
  .nav-menu { display: flex; }
}

.nav-link {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #525252;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-link:hover { color: #171717; }
.nav-link.active { color: #9333ea; font-weight: 700; }

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Mobile menu styles */
#mobile-menu {
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

#mobile-menu a,
#mobile-menu button {
  transition: all 0.2s ease;
}

#mobile-menu a:hover,
#mobile-menu button:hover {
  transform: translateX(4px);
}

/* Hide desktop buttons on mobile */
@media (max-width: 639px) {
  .btn-ghost.hidden,
  .btn-primary.hidden {
    display: none !important;
  }
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  text-decoration: none;
}

.btn-ghost {
  background-color: rgba(255, 255, 255, 0.6);
  color: #171717;
  border: 1px solid #e5e5e5;
}

.btn-ghost:hover {
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.35);
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.45);
}

.btn-primary:hover::before {
  left: 100%;
}

/* Main Content */
.main-content {
  padding-top: 6rem;
  padding-bottom: 4rem;
}

.card {
  border-radius: 1.5rem;
  border: 1px solid rgba(229, 229, 229, 0.7);
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: 0 20px 60px -20px rgba(10, 10, 10, 0.2);
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card:hover {
  box-shadow: 0 25px 80px -25px rgba(10, 10, 10, 0.25);
  border-color: rgba(212, 212, 212, 0.8);
  transform: translateY(-4px);
}

.card:hover::before {
  opacity: 1;
}

.hero-section {
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.08) 0%, rgba(219, 39, 119, 0.05) 100%);
  padding: 3rem 2rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -25%;
  width: 50%;
  height: 200%;
  background: radial-gradient(circle, rgba(147, 51, 234, 0.1) 0%, transparent 70%);
  transform: rotate(45deg);
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #737373;
  background: rgba(23, 23, 23, 0.06);
  border: 1px solid rgba(23, 23, 23, 0.1);
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  margin-bottom: 1rem;
}

h1 {
  font-size: 2.25rem;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin: 0 0 1rem 0;
}

@media (min-width: 640px) {
  h1 { font-size: 3rem; }
}

.subtitle {
  color: #737373;
  font-size: 1.125rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.subtitle b {
  color: #171717;
  font-weight: 600;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.kpi-card {
  background: rgba(23, 23, 23, 0.03);
  border: 1px solid rgba(23, 23, 23, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  text-align: center;
}

.kpi-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #171717;
}

.kpi-label {
  color: #737373;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  letter-spacing: -0.01em;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .grid-2 { grid-template-columns: 1fr 1fr; }
}

.feature-card {
  padding: 1.5rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.feature-card p {
  color: #737373;
  line-height: 1.6;
  margin: 0;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 0.75rem;
  counter-reset: step;
}

.step-card {
  padding: 1.25rem;
  position: relative;
  counter-increment: step;
}

.step-card::before {
  content: counter(step);
  position: absolute;
  left: -0.5rem;
  top: -0.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  width: 2rem;
  height: 2rem;
  border-radius: 9999px;
  display: grid;
  place-items: center;
  font-weight: 700;
  border: 3px solid #fafafa;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.step-card h4 {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.step-card p {
  color: #737373;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.price-card {
  background: linear-gradient(180deg, rgba(34, 197, 94, 0.08), transparent);
  padding: 1.5rem;
  position: relative;
  text-align: center;
}

.price-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.price-card:hover::after {
  transform: scaleX(1);
}

.price-card h4 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.price-card p {
  color: #737373;
  font-size: 0.95rem;
  margin: 0 0 0.75rem 0;
}

.price-value {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.note {
  background: rgba(23, 23, 23, 0.04);
  border: 1px dashed rgba(23, 23, 23, 0.2);
  padding: 1rem;
  border-radius: 0.75rem;
  color: #737373;
  font-size: 0.95rem;
  line-height: 1.6;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid rgba(23, 23, 23, 0.1);
  background: rgba(23, 23, 23, 0.03);
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #171717;
  font-weight: 600;
}

.faq-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.faq-card {
  padding: 1.25rem;
}

.faq-q {
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.faq-a {
  color: #737373;
  line-height: 1.6;
}

.cta-section {
  text-align: center;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(23, 23, 23, 0.1);
}

.cta-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.footer-note {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(23, 23, 23, 0.1);
  color: #737373;
  font-size: 0.875rem;
  text-align: center;
}

/* Lists */
.feature-list {
  margin: 0;
  padding-left: 1.25rem;
  color: #525252;
}

.feature-list li {
  margin: 0.5rem 0;
  line-height: 1.6;
}
	.wpcf7-form button {
		border: none;
		cursor: pointer;
	}
	input.wpcf7-form-control {
		    width: calc(100% - 4rem);
	}
	.hide-block {
		display: none;
	}
</style>

<!-- Navigation Header -->
<div class="nav-header">
  <div class="nav-container">
    <div class="nav-bar">
      <nav class="nav-content">
        <a href="<?php echo home_url(); ?>" class="nav-logo">
          <span class="nav-logo-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7V12C2 18.5 6.5 21.7 12 22C17.5 21.7 22 18.5 22 12V7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span class="nav-logo-text">GoIP Pro</span>
        </a>

        <div class="nav-menu">
          <a href="<?php echo home_url('/#about'); ?>" class="nav-link">О компании</a>
          <a href="<?php echo home_url('/#start-steps'); ?>" class="nav-link">Как начать</a>
          <a href="<?php echo home_url('/goip-technology/'); ?>" class="nav-link active">Технология GoIP</a>
          <a href="<?php echo home_url('/#earnings'); ?>" class="nav-link">Доходы</a>
          <a href="<?php echo home_url('/blog'); ?>" class="nav-link">Новости</a>
          <a href="<?php echo home_url('/#faq'); ?>" class="nav-link">FAQ</a>
        </div>

        <div class="nav-actions">
          <?php echo do_shortcode('[gtranslate]'); ?>
          
                         <!-- Desktop auth buttons - hidden on mobile -->
               <a href="#" class="btn btn-ghost mobile-hide-auth" onclick="openAuthModal(event)">Войти</a>
               <a href="#" class="btn btn-primary mobile-hide-auth" onclick="openAuthModal(event)">Регистрация</a>
          
          <!-- Mobile menu button -->
          <button id="mobile-menu-btn" class="sm:hidden p-2 rounded-lg hover:bg-neutral-100 transition-colors">
            <svg id="menu-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg id="close-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: none;">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </nav>
      
      <!-- Mobile dropdown menu -->
      <div id="mobile-menu" class="sm:hidden border-t border-neutral-200/60 bg-white/90 backdrop-blur-md rounded-b-2xl" style="display: none;">
        <div class="px-3 py-4 space-y-3">
          <!-- Navigation links -->
          <a href="<?php echo home_url('/#about'); ?>" class="block px-3 py-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors rounded-lg hover:bg-neutral-50">
            О компании
          </a>
          <a href="<?php echo home_url('/#start-steps'); ?>" class="block px-3 py-2 text-sm font-medium text-purple-600 font-bold hover:text-purple-700 transition-colors rounded-lg hover:bg-purple-50">
            Как начать
          </a>
          <a href="<?php echo home_url('/goip-technology/'); ?>" class="block px-3 py-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors rounded-lg hover:bg-neutral-50">
            Технология GoIP
          </a>
          <a href="<?php echo home_url('/#earnings'); ?>" class="block px-3 py-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors rounded-lg hover:bg-neutral-50">
            Доходы
          </a>
          <a href="<?php echo home_url('/blog'); ?>" class="block px-3 py-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors rounded-lg hover:bg-neutral-50">
            Новости
          </a>
          <a href="<?php echo home_url('/#faq'); ?>" class="block px-3 py-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors rounded-lg hover:bg-neutral-50">
            FAQ
          </a>
          
          <!-- Auth buttons -->
          <div class="pt-2 border-t border-neutral-200/60">
            <button onclick="openAuthModal(event)" class="w-full text-left px-3 py-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors rounded-lg hover:bg-neutral-50">
              Войти
            </button>
            <button onclick="openAuthModal(event)" class="w-full text-left px-3 py-2 text-sm font-medium text-purple-600 font-bold hover:text-purple-700 transition-colors rounded-lg hover:bg-purple-50">
              Регистрация
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Main Content -->
<main class="main-content">
  <div class="container-tight">
    
    <!-- Hero Section -->
    <section class="card hero-section">
      <div style="display: flex; flex-wrap: wrap; gap: 3rem; align-items: center;">
        <div style="flex: 1 1 60%; min-width: 300px;">
          <span class="eyebrow">goippro.com • партнёрская программа</span>
          <h1>Ваш грузовик зарабатывает сам: пассивный доход с GoIP шлюзом</h1>
          <p class="subtitle">Установите компактный GoIP в кабину, подключите SIM — и получайте <b>ежемесячные выплаты</b> от партнёра goippro.com. Никакой рутины и отвлечения от рейсов: устройство работает, пока вы в пути.</p>
          
          <div class="cta-buttons">
            <a href="#" class="btn btn-primary" onclick="openReactAuthModal(event)">Стать партнёром</a>
            <a href="#how" class="btn btn-ghost">Как это работает</a>
          </div>
        </div>
        <div style="flex: 1 1 35%; min-width: 250px; text-align: center;">
          <img src="<?php echo get_stylesheet_directory_uri(); ?>/track.png" alt="GoIP в грузовике" style="max-width: 100%; height: auto; filter: drop-shadow(0 10px 30px rgba(147, 51, 234, 0.3));">
        </div>
      </div>
      
      <div class="kpi-grid">
        <div class="kpi-card">
          <span class="kpi-value">от $150/мес</span>
          <span class="kpi-label">типичный доход по базовому тарифу</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-value">10 минут</span>
          <span class="kpi-label">среднее время установки</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-value">EU/EAEU</span>
          <span class="kpi-label">соответствие и легальность эксплуатации</span>
        </div>
      </div>
    </section>

    <!-- Why It's Profitable -->
    <section class="section">
      <h2 class="section-title">Почему это выгодно дальнобойщикам</h2>
      <div class="grid-2">
        <div class="card feature-card">
          <div class="feature-icon icon-gradient-1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3>Пассивный доход без лишних действий</h3>
          <p>Пока вы едете и меняете базовые станции, GoIP обеспечивает стабильную работу — и стабильные начисления. Зарплата идёт своим чередом, а шлюз приносит сверху.</p>
        </div>
        <div class="card feature-card">
          <div class="feature-icon icon-gradient-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3>Легально и прозрачно</h3>
          <p>Используем сертифицированное оборудование и белые процессы. Все документы доступны в личном кабинете партнёра.</p>
        </div>
        <div class="card feature-card">
          <div class="feature-icon icon-gradient-3">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3>Работает в пути и в роуминге</h3>
          <p>Мобильность — ваше преимущество: смена сот, стран и операторов повышает устойчивость работы и прогнозируемость выплат.</p>
        </div>
        <div class="card feature-card">
          <div class="feature-icon icon-gradient-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          </div>
          <h3>Офлайн-буферизация</h3>
          <p>В «глухих» зонах шлюз копит данные локально и синхронизирует их при появлении связи — начисления не теряются.</p>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="section" id="how">
      <h2 class="section-title">Как это работает: 3 шага</h2>
      <div class="steps-grid">
        <div class="card step-card">
          <h4>Установка</h4>
          <p>Крепим шлюз в кабине, подаём питание 12/24 V, вставляем SIM. Вся процедура занимает около 10 минут.</p>
        </div>
        <div class="card step-card">
          <h4>Активация</h4>
          <p>Авторизуем устройство в системе goippro.com, проверяем связь. Доступ к личному кабинету — сразу.</p>
        </div>
        <div class="card step-card">
          <h4>Начисления</h4>
          <p>Шлюз работает автономно. Доход начисляется ежедневно, вывод — раз в месяц на удобный вам способ.</p>
        </div>
      </div>
    </section>

    <!-- Earnings -->
    <section class="section">
      <h2 class="section-title">Сколько можно заработать</h2>
      <div class="pricing-grid">
        <div class="card price-card">
          <h4>Basic</h4>
          <p>Маршруты внутри одной страны, средняя занятость.</p>
          <span class="price-value">$100–$150 / мес</span>
        </div>
        <div class="card price-card">
          <h4>Pro</h4>
          <p>Пересечение границ, активные рейсы, устойчивое покрытие.</p>
          <span class="price-value">$150–$250 / мес</span>
        </div>
        <div class="card price-card">
          <h4>Max</h4>
          <p>Длинные международные рейсы и высокая мобильность.</p>
          <span class="price-value">$250–$450 / мес</span>
        </div>
      </div>
      <p class="note">Фактический доход зависит от маршрутов, качества связи, тарифов операторов и режима работы. Подробный расчёт доступен в личном кабинете партнёра.</p>
    </section>

    <!-- ROI Calculator -->
    <section class="section">
      <h2 class="section-title">Калькулятор окупаемости (пример)</h2>
      <div class="grid-2">
        <div class="card feature-card">
          <h3>Предпосылки расчёта</h3>
          <ul class="feature-list">
            <li>Стоимость 4‑портового GoIP — около 200 €;</li>
            <li>Доход с одной SIM — $10 в месяц (≈ $300 в месяц при 30 днях);</li>
            <li>Полная загрузка портов, стабильное покрытие и питание.</li>
          </ul>
        </div>
        <div class="card feature-card">
          <h3>Итоги</h3>
          <ul class="feature-list">
            <li>4 порта: 4 × $300 = <b>$1 200 / 10 месяцев</b> — окупаемость «железки» <b>&lt; 1 месяца</b>;</li>
            <li>8 портов: 8 × $300 = <b>$2 400 / 10 месяцев</b>;</li>
            <li>16 портов: 16 × $300 = <b>$4 800 / 10 месяцев</b>.</li>
          </ul>
        </div>
      </div>
      <p class="note">Это ориентиры при полной загрузке и выбранной модели $10/месяц на SIM. Реальные значения зависят от тарифов, маршрутов, качества связи и требований операторов. В нашем кабинете будет доступен удобный калькулятор по портам (4/8/16) и сценариям использования.</p>
    </section>

    <!-- Rating System -->
    <section class="section">
      <h2 class="section-title">Система рейтингов и работа с менеджерами</h2>
      <div class="grid-2">
        <div class="card feature-card">
          <h3>Рейтинг партнёра</h3>
          <p>В системе goippro.com действует автоматическая рейтинговая модель, которая определяет лояльность партнёра. <b>Лояльный партнёр</b> — это тот, у кого оборудование работает стабильно, есть доступ к интернету, пополнены балансы, а также партнёр оперативно отвечает на сообщения в кабинете.</p>
        </div>
        <div class="card feature-card">
          <h3>Персональный менеджер</h3>
          <p>За каждым партнёром закрепляется персональный менеджер. Дополнительно на линии находятся ещё два менеджера, чтобы быстро реагировать на запросы 24/7.</p>
        </div>
      </div>
      <div class="card feature-card" style="margin-top: 1rem;">
        <h3>Типовые запросы</h3>
        <ul class="feature-list">
          <li>изменение тарифов и добавление услуг;</li>
          <li>подбор стран/регионов работы;</li>
          <li>приобретение дополнительного оборудования и ресурсов;</li>
          <li>диагностика и мониторинг (локально или удалённо).</li>
        </ul>
      </div>
    </section>

    <!-- Requirements -->
    <section class="section">
      <h2 class="section-title">Требования и условия</h2>
      <div class="grid-2">
        <div class="card feature-card">
          <h3>Минимальные требования</h3>
          <ul class="feature-list">
            <li>Питание 12/24 V в кабине и защищённое место крепления;</li>
            <li>SIM-карта(ы) с подходящим тарифом и разрешённым режимом использования;</li>
            <li>Базовое покрытие сотовой связи на маршрутах;</li>
            <li>Соблюдение температурных режимов и вентиляции места установки.</li>
          </ul>
        </div>
        <div class="card feature-card">
          <h3>Юридически важно</h3>
          <ul class="feature-list">
            <li>Эксплуатация оборудования осуществляется в рамках законодательства вашей страны и условий операторов;</li>
            <li>Доступен комплект документов: сертификаты, договор/оферта, памятка водителю;</li>
            <li>При проверке на дороге вы можете показать паспорт устройства и инструкцию.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Referral Program -->
    <section class="section">
      <h2 class="section-title">Реферальная программа</h2>
      <div class="card feature-card">
        <p><span class="badge">+10% пожизненно</span> к вашим выплатам за каждого приглашённого партнёра-водителя. Вознаграждения начисляются автоматически, лимитов нет.</p>
      </div>
    </section>

    <!-- FAQ -->
    <section class="section">
      <h2 class="section-title">Частые вопросы</h2>
      <div class="faq-grid">
        <div class="card faq-card">
          <div class="faq-q">Это легально?</div>
          <div class="faq-a">Да. Мы используем сертифицированные устройства и стандартные интерфейсы. Важно использовать SIM-карты и тарифы, разрешающие заявленный режим. Пакет документов предоставим.</div>
        </div>
        <div class="card faq-card">
          <div class="faq-q">Что если пропадает связь?</div>
          <div class="faq-a">Шлюз буферизует данные и синхронизирует их при восстановлении сети. Начисления сохраняются.</div>
        </div>
        <div class="card faq-card">
          <div class="faq-q">Как происходят выплаты?</div>
          <div class="faq-a">Фиксируем начисления ежедневно, выплачиваем раз в месяц на карту/счёт. График и способы — в договоре/оферте.</div>
        </div>
        <div class="card faq-card">
          <div class="faq-q">Есть ли поддержка?</div>
          <div class="faq-a">Да, техподдержка 24/7, Telegram‑чат с действующими партнёрами и база знаний в личном кабинете.</div>
        </div>
      </div>
    </section>



    <!-- CTA -->
    <div class="cta-section">
      <h2 class="section-title">Готовы начать зарабатывать?</h2>
      <div class="cta-buttons">
        <a href="#" class="btn btn-primary" onclick="openReactAuthModal(event)">Подключиться сейчас</a>
        <a href="#" class="btn btn-ghost" onclick="openReactAuthModal(event)">Связаться с менеджером</a>
      </div>
    </div>

    <div class="footer-note">
      © goippro.com. Технология GoIP для партнёров-дальнобойщиков.
    </div>
    
  </div>
</main>


<div id="react-auth-modal" class="hide-block fixed  inset-0 z-50 flex items-center justify-center animate-in">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-3xl shadow-2xl max-w-md w-full mx-4 overflow-hidden">
        <div class="bg-gradient-to-r from-purple-600 via-pink-600 to-orange-600 p-6 text-white relative">
          <button onclick="closeReactAuthModal()" class="close-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
          <div class="text-center">
            <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <h2 class="text-2xl font-bold mb-2">Регистрация в системе</h2>
            <p class="text-white/90">Создайте аккаунт для начала работы</p>
          </div>
        </div>
        <div class="p-6">
<?php echo do_shortcode('[contact-form-7 id="ff23568" title="Контактная форма 1"]'); ?>
          <div class="mt-6 text-center space-y-3">
            
           
          </div>
        </div>
      </div>
    </div>

<script>
function openAuthModal(event) {
  event.preventDefault();
  
  // Try to find React app's auth modal trigger
  const authTrigger = document.querySelector('[data-auth-trigger]');
  if (authTrigger) {
    authTrigger.click();
    return;
  }
  
  // Dispatch custom event that React might be listening to
  window.dispatchEvent(new CustomEvent('openAuthModal'));
  
  // If React app is available, try to call its method
  if (window.openAuthModal && typeof window.openAuthModal === 'function') {
    window.openAuthModal();
  }
  
  // Fallback: redirect to home page with auth parameter
  if (!authTrigger && !window.openAuthModal) {
    window.location.href = '/?auth=open';
  }
}

function openReactAuthModal(event) {
  event.preventDefault();
  
  // Create and show React-style auth modal
  showReactAuthModal();
}

function showReactAuthModal() {
  // Remove existing modal if any
  const existingModal = document.getElementById('react-auth-modal');
  
  // Prevent body scroll
  document.body.style.overflow = 'hidden';
  if (existingModal) {
    existingModal.classList.remove('hide-block');
    // Обновить содержимое модального окна, если нужно
    // existingModal.innerHTML = 'Новое содержимое';
  } else {
    // Создать и добавить новое модальное окно, если его нет
    // ... (ваш код для создания модального окна)
  }

  // Focus on phone input
  setTimeout(() => {
    const phoneInput = document.getElementById('phone');
    if (phoneInput) phoneInput.focus();
  }, 100);
}

function closeReactAuthModal() {
  const modal = document.getElementById('react-auth-modal');
  if (modal) {
    modal.classList.add('hide-block');
    document.body.style.overflow = 'unset';
  }
}


// Listen for React app to be ready
document.addEventListener('DOMContentLoaded', function() {
  // Check if we need to open auth modal from URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('auth') === 'open') {
    setTimeout(() => openAuthModal(new Event('click')), 500);
  }
  
  // Mobile menu functionality
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuIcon = document.getElementById('menu-icon');
  const closeIcon = document.getElementById('close-icon');
  
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', function() {
      const isOpen = mobileMenu.style.display !== 'none';
      
      if (isOpen) {
        mobileMenu.style.display = 'none';
        menuIcon.style.display = 'block';
        closeIcon.style.display = 'none';
      } else {
        mobileMenu.style.display = 'block';
        menuIcon.style.display = 'none';
        closeIcon.style.display = 'block';
      }
    });
  }
});
</script>

<?php get_footer(); ?>
