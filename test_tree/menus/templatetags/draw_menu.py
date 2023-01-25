from django import template
from django.utils.safestring import mark_safe
from django.db.models import QuerySet

from menus.models import Field, Menu

register = template.Library()

SPACER = "$$"
HREF_SPACER = "$href$"
UL = f"<ul>{SPACER}</ul>"
LI = f"<li>{SPACER}</li>"
A = f"<a href={HREF_SPACER}>{SPACER}</a>"

TagHTML = dict[str, str]
RawHTML = str  # generated html code


@register.inclusion_tag('draw_menu.html')
def drow_menu(splited_menu: list[str]) -> TagHTML:
    """The main templatetag function, preparing tree menu by making request
    to and draw via raw html."""
    if splited_menu == ['all']:
        return _show_all_menus()
    menu_name = splited_menu.pop(0)
    fields = Field.objects.filter(menu__slug=menu_name)
    header = _draw_head(menu_name, fields)
    menu_html = _draw_levels(header, fields, splited_menu)
    menu = mark_safe(menu_html)
    return {'menu': menu}


def _show_all_menus() -> TagHTML:
    """Function for drawing all menus."""
    menus = Menu.objects.all().values_list('name', 'slug')
    raw_html = ''
    for menu_name in menus:
        raw_html += _draw_html_ul_level(menu_name[0], menu_name[1])
        menu = mark_safe(raw_html)
    return menu


def _draw_head(menu_name: str, fields: QuerySet) -> RawHTML:
    """Draw first levels of menu, that include top fields and menu names."""
    raw_html = _draw_html_ul_level(menu_name, menu_name)
    previous_elem = f'{menu_name}</a>'  # for find place for new level insert
    slugs = list(fields.filter(is_head=True).values_list('name', 'slug'))
    for slug in slugs:
        child = fields.filter(parents__parent__name=slug[0]).first().slug
        href = menu_name + "_" + slug[1] + "_" + child
        header = _draw_html_ul_level(slug[0], href)
        raw_html = _concatinate_levels(previous_elem, raw_html, header)
    return raw_html


def _draw_html_ul_level(value: str, href: str) -> RawHTML:
    """Create html code for the new level of menu"""
    raw_html = A.replace(SPACER, value)
    raw_html = raw_html.replace(HREF_SPACER, href)
    raw_html = LI.replace(SPACER, raw_html)
    raw_html = UL.replace(SPACER, raw_html)
    return raw_html


def _concatinate_levels(
    previous: str, main_html: RawHTML, new_level_html: RawHTML
) -> RawHTML:
    """Concatenate (insert) new level inside a main html code."""
    index = main_html.find(previous) + len(previous)
    html = main_html[:index] + new_level_html + main_html[index:]
    return html


def _draw_levels(
    main_html: RawHTML, fields: QuerySet, splited_menu: list[str]
) -> RawHTML:
    """Create new html code for levels under top menu fields"""
    menu_without_last_field = splited_menu[:-1]
    for level in menu_without_last_field:
        slugs = list(fields.filter(
            parents__parent__slug=level
        ).values_list('name', flat=True))
        name = fields.get(slug=level).name
        for slug in slugs:
            child = fields.get(name=slug).childs.first()
            if child:
                href = child.url
            else:
                href = fields.first().menu.slug + '_' + '_'.join(
                    menu_without_last_field
                )
            new_ul_level = _draw_html_ul_level(slug, href)
            main_html = _concatinate_levels(name, main_html, new_ul_level)
    return main_html
