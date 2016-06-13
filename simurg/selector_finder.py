def find_selector(soup, el):
    """Given a parsed html document, find a css selector for the given element.

    # Arguments
        soup: parsed html document
        el: html element for which a css selector has to be found

    # Returns
        selector: a css selector (or None if nothing found)
    """
    css_selectors = [class_css_selector, id_css_selector, type_css_selector]
    for selector in css_selectors:
        css_selector = selector(el)
        if valid(soup, css_selector) and \
                unique(soup, css_selector) and \
                match(soup, css_selector, el):
            return css_selector
    return None


def id_css_selector(el):
    """Tries to construct a css selector of the form el#id from the element

    # Argument
        el: an html element

    # Returns
        selector: css selector of the form el#id
    """
    css_id = el.get('id', None)
    if css_id and len(css_id[0].strip()) > 0:
        return '{}#{}'.format(el.name, css_id[0])
    return None


def class_css_selector(el):
    """Tries to construct a css selector of the form el.class from the element

    # Argument
        el: an html element

    # Returns
        selector: css selector of the form el.class
    """
    css_class = el.get('class', None)
    if css_class and len(css_class[0].strip()) > 0:
        return '{}.{}'.format(el.name, css_class[0])
    return None


def type_css_selector(el):
    """Tries to construct a css selector of the form el from the element

    # Argument
        el: an html element

    # Returns
        selector: css selector of the form el
    """
    if el.name:
        return '{}'.format(el.name)
    return None


def unique(soup, css_selector):
    """Checks if selecting the css selector returns a unique element.

    # Arguments
        soup: parsed html document
        css_selector: css selector to be tested

    # Returns
        unique: True if a unique element is returned
    """
    return len(list(soup.select(css_selector))) == 1


def valid(soup, css_selector):
    """Checks if the css selector is valid.

    # Arguments
        soup: parsed html document
        css_selector: css selector for which the validity has to be checked

    # Returns
        valid: True if css slector is valid
    """
    try:
        soup.select(css_selector)
        return True
    except:
        return False


def match(soup, css_selector, el):
    """Checks if the selected element by the css selector matches
    the given element.

    # Arguments
        soup: parsed html document
        css_selector: css selector that returns an element
        el: html element to be matched with
    """
    return soup.select(css_selector)[0] == el
