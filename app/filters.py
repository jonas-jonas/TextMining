from services.analyzer import is_being_analyzed

def polarity_class(polarity):
    if polarity is None:
        return ''
    if polarity < -.333:
        return 'error'
    elif polarity < .333:
        return 'warn'
    else:
        return 'success'

def subjectivity_class(subjectivity):
    if subjectivity is None:
        return ''
    if subjectivity < .333:
        return 'success'
    elif subjectivity < .666:
        return 'warn'
    else:
        return 'error'
