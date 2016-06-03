def el_to_css_selector(soup, el):
    css_selectors = [class_css_selector, id_css_selector, type_css_selector]
    for selector in css_selectors:
        css_selector = selector(el)
        if valid(soup, css_selector) and \
                unique(soup, css_selector) and \
                match(soup, css_selector, el):
            return css_selector
    return None


def id_css_selector(el):
    css_id = el.get('id', None)
    if css_id:
        return '{}#{}'.format(el.name, css_id)
    return None


def class_css_selector(el):
    css_class = el.get('class', None)
    if css_class:
        return '{}.{}'.format(el.name, css_class)
    return None


def type_css_selector(el):
    if el.name:
        return '{}'.format(el.name)
    return None


def unique(soup, css_selector):
    return len(list(soup.select(css_selector))) == 1


def valid(soup, css_selector):
    try:
        soup.select(css_selector)
        return True
    except:
        return False


def match(soup, css_selector, el):
    return soup.select(css_selector)[0] == el
