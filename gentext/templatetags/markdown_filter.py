from django import template
import markdown

register = template.Library()


@register.filter
def markdownify(text):
    md = markdown.Markdown(
        extensions=['markdown.extensions.toc'],
        safe_mode='escape'
    )
    return md.convert(text)
