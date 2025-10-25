# Hugo Blog with Ananke Theme - AI Assistant Instructions

## Project Overview

This is a Hugo static site using the **Ananke theme** (v2.12.1), designed for blogging with responsive design, social media integration, and Tachyons CSS utility classes.

## Architecture & Key Components

### Theme Structure
- **Base site config**: `hugo.toml` (minimal configuration)
- **Theme source**: `themes/ananke/` (Git submodule/download)
- **Theme config**: `themes/ananke/config/_default/` contains Hugo and params configuration
- **Custom overrides**: Create files in root `/layouts/` and `/assets/` to override theme defaults

### CSS Processing Pipeline
- **Framework**: Tachyons CSS utility classes (`themes/ananke/assets/ananke/css/`)
- **Build process**: Hugo Pipes concatenates `_tachyons.css`, `_code.css`, `_hugo-internal-templates.css`, `_social-icons.css`, `_styles.css`
- **Custom CSS**: Add files to `assets/ananke/css/` and register in `hugo.toml`:
  ```toml
  [params]
  custom_css = ["custom.css", "special.css"]
  ```
- **SCSS support**: Requires Hugo Extended for Sass/SCSS processing

### Content Management
- **Archetypes**: Use `archetypes/default.md` template for new content
- **Front matter**: TOML format with `date`, `draft`, `title`, `featured_image` etc.
- **Featured images**: Support for both static paths and Page Resources (place in content folder)

## Essential Development Workflows

### Local Development
```bash
hugo server           # Start dev server on localhost:1313
hugo new posts/title.md  # Create new post using archetype
hugo                  # Build static site to /public/
```

### Content Creation Patterns
- **Posts**: Place in `content/posts/` directory
- **Pages**: Place in `content/` or organize in subdirectories
- **Images**: Use `static/images/` for static assets or Page Resources co-located with content
- **Draft workflow**: Set `draft = true` in front matter, use `hugo server -D` to preview

### Theme Customization Strategy
1. **Never edit theme files directly** - they'll be overwritten on updates
2. **Override layouts**: Copy from `themes/ananke/layouts/` to root `layouts/` with same path
3. **Custom partials**: Create in `layouts/partials/` (e.g., `head-additions.html` for custom scripts)
4. **Asset overrides**: Place in `assets/ananke/css/` and register via `custom_css` parameter

## Project-Specific Conventions

### Configuration Patterns
- **Site-wide settings**: Use `hugo.toml` for basic config, theme handles advanced features via `themes/ananke/config/_default/params.toml`
- **Social media**: Extensive social network configuration in theme params - enable by listing in `networks` arrays
- **Styling classes**: Use Tachyons utilities (`bg-blue`, `avenir`, `cover bg-center`) for customization
- **Environment detection**: Theme automatically handles production vs development (robots.txt, analytics, minification)

### Front Matter Standards
```toml
date = '2024-10-25T10:00:00Z'
draft = false
title = 'Post Title'
featured_image = '/images/hero.jpg'  # or Page Resource filename
omit_header_text = true              # hide title overlay on featured image
text_color = "green"                 # Tachyons color class
canonicalUrl = "https://original.com/post"  # for republished content
```

### Social Media Integration
- **Follow links**: Configure in `[ananke.social.follow]` with `networks = ["facebook", "twitter"]`
- **Share buttons**: Configure in `[ananke.social.share]` with customizable icons and text
- **Custom networks**: Full configuration available in `themes/ananke/config/_default/params.toml`

## Key Files for Common Tasks

### Styling Changes
- `assets/ananke/css/custom.css` - Custom CSS additions
- `hugo.toml` - Body classes (`body_classes = "avenir bg-near-white"`)
- `layouts/partials/head-additions.html` - Custom head scripts/styles

### Layout Modifications
- `layouts/_default/baseof.html` - Site structure override
- `layouts/partials/site-header.html` - Navigation customization
- `layouts/index.html` - Homepage layout override

### Content Organization
- `content/` - All site content (currently empty - needs setup)
- `static/images/` - Static assets
- `archetypes/default.md` - New content template

## Integration Points

### Theme Dependencies
- **Minimum Hugo version**: 0.128.0
- **Tachyons CSS**: v4.12.0 (utility-first CSS framework)
- **Font Awesome**: For social media icons (Creative Commons licensed)

### Build Requirements
- **Hugo Extended**: Required for SCSS processing in custom CSS
- **PostCSS**: Theme includes cssnano and postcss-preset-env for CSS optimization
- **Git submodule**: Theme managed as external dependency

### External Services Integration
- **Analytics**: Hugo internal template integration
- **Comments**: Supports Disqus and Commento
- **Forms**: Contact form shortcode with Formspree.io integration
- **SEO**: Built-in OpenGraph, Schema.org, and Twitter Cards

## Common Pitfalls to Avoid

1. **Don't edit theme files directly** - use override patterns instead
2. **Hugo Extended required** for SCSS custom CSS - document this dependency
3. **Social media config** is complex - refer to theme's params.toml for exact syntax
4. **Featured images** - understand difference between static paths vs Page Resources
5. **Production builds** - ensure proper baseURL in hugo.toml for deployment