class Resource(object):
    def __init__(self, doc):
        self.doc = doc
        self.self = doc.self
        self.class_ = doc.meta.class_

    @property
    def edited(self):
        return self.doc.meta.edited

    @property
    def created(self):
        return self.doc.meta.created

    @property
    def hash(self):
        return self.doc.meta.hash

    @property
    def id(self):
        return self.doc.meta.id

    @property
    def content(self):
        return self.doc.content

    def related(self, relation, class_=None):
        rel = self.doc.related(relation, class_)
        return rel.specialize()


class Collection(object):
    def __init__(self, doc):
        self.doc = doc


class Service(object):
    def __init__(self, doc):
        self.doc = doc
