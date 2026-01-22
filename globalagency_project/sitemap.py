"""
Sitemap configuration for SEO optimization
Supports multilingual sitemap generation
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils.translation import activate, get_language


class StaticPagesSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        """Return list of static pages"""
        return ['home', 'about', 'services', 'contact', 'courses']

    def location(self, item):
        """Generate URL for each item"""
        return reverse(item)

    def lastmod(self, item):
        """Return last modified date - can be extended with actual dates"""
        from datetime import datetime
        return datetime.now()


class UniversitiesSitemap(Sitemap):
    """Sitemap for university listings"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        """Return list of universities - extend with actual model"""
        # This would query your University model if you have one
        # For now returning example items
        return [
            {'id': 1, 'name': 'Example University 1'},
            {'id': 2, 'name': 'Example University 2'},
        ]

    def location(self, item):
        """Generate URL for each university"""
        return f'/universities/{item["id"]}/'

    def lastmod(self, item):
        """Return last modified date"""
        from datetime import datetime
        return datetime.now()


class CoursesSitemap(Sitemap):
    """Sitemap for course listings"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        """Return list of courses"""
        courses = [
            {'id': 1, 'slug': 'computer-science'},
            {'id': 2, 'slug': 'business-management'},
            {'id': 3, 'slug': 'healthcare-medical'},
            {'id': 4, 'slug': 'engineering'},
            {'id': 5, 'slug': 'data-science'},
            {'id': 6, 'slug': 'law'},
        ]
        return courses

    def location(self, item):
        """Generate URL for each course"""
        return f'/courses/{item["slug"]}/'

    def lastmod(self, item):
        """Return last modified date"""
        from datetime import datetime
        return datetime.now()


class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        """Return list of blog posts"""
        # This would query your BlogPost model if you have one
        return []

    def location(self, item):
        """Generate URL for each blog post"""
        return f'/blog/{item.slug}/'

    def lastmod(self, item):
        """Return last modified date"""
        return item.updated_at if hasattr(item, 'updated_at') else item.created_at


# Sitemap configuration dictionary
sitemaps = {
    'static': StaticPagesSitemap,
    'universities': UniversitiesSitemap,
    'courses': CoursesSitemap,
    'blog': BlogSitemap,
}
