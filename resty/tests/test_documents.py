import unittest2 as unittest


class TestDictDocument(unittest.TestCase):

    def _get_target(self):
        from resty.documents import DictDocument
        return DictDocument

    def _make_one(self, meta={}, content={}):
        meta_copy = dict(('$%s' % key, value) for key, value in meta.items())
        meta_copy.update(content)
        return self._get_target()(meta_copy, content)

    def test_empty_json(self):
        self.assertRaises(ValueError, self._make_one)

    def test_required_fields(self):
        self.assertRaises(ValueError, self._make_one,
            content={'a': 'a', 'b': 'b'}
        )
        self.assertRaises(ValueError, self._make_one,
            meta={'type': 'type'}
        )
        self.assertRaises(ValueError, self._make_one,
            meta={'self': 'self'}
        )

    def test_minimal_doc(self):
        d = self._make_one(meta={'type': 'type', 'self': 'self'})
        self.assertEqual(d.type, 'type')
        self.assertEqual(d.self, 'self')
        self.assertRaises(AttributeError, getattr, d.meta, 'type')
        self.assertRaises(AttributeError, getattr, d.meta, 'self')

    def test_meta_attrs(self):
        d = self._make_one(
            meta={'type': 'type', 'self': 'self', 'a': 'a', 'b': 'b'}
        )
        self.assertEqual(d.meta.a, 'a')
        self.assertEqual(d.meta.b, 'b')

    def test_content_attrs(self):
        d = self._make_one(
            meta={'type': 'type', 'self': 'self'}, content={'a': 'a', 'b': 'b'}
        )
        self.assertEqual(d.content.a, 'a')
        self.assertEqual(d.content.b, 'b')

    def test_attr_errors(self):
        d = self._make_one(
            meta={'type': 'type', 'self': 'self', 'a': 'a'}, content={'b': 'b'}
        )
        self.assertEqual(d.meta.a, 'a')
        self.assertEqual(d.content.b, 'b')
        self.assertRaises(AttributeError, getattr, d.content, 'a')
        self.assertRaises(AttributeError, getattr, d.meta, 'b')

    def test_complex_structure(self):
        d = self._make_one(
            meta={'type': 'type', 'self': 'self'},
            content={'a': [1, 'a'], 'b': {'x': 'x', 1: 1}}
        )
        self.assertEqual(d.content.a, [1, 'a'])
        self.assertEqual(d.content.b, {'x': 'x', 1: 1})
        self.assertRaises(AttributeError, getattr, d.content.b, 'x')

    def test_filters(self):
        d = self._make_one(
            meta={
                'type': 'type',
                'self': 'self',
                'filters': {
                    'filter1': 'f1{placeholder1}{placeholder2}',
                    'filter2': 'f2',
                },
            },
        )

        f = d.get_filter_uri(d, 'filter1', placeholder1='a', placeholder2='b')
        self.assertEqual(f, 'f1ab')

        f = d.get_filter_uri(d, 'filter2')
        self.assertEqual(f, 'f2')


# from resty.tests.mocks import MockStateMachine, MockDocument

# class TestLazyDocument(unittest.TestCase):

#     def setUp(self):
#         self.sm = MockStateMachine()
#         doc = MockDocument(meta={'b': 'b'}, content={'a': 'a', 'x': 'x'})
#         self.sm.add_state('test://partial_object', doc)

#     def _get_target(self):
#         from resty.documents import LazyDocument
#         return LazyDocument

#     def _make_one(self, meta={}, content={}):
#         meta_copy = dict(('$%s' % key, value) for key, value in meta.items())
#         meta_copy.update(content)
#         return self._get_target()(meta_copy, self.sm)

#     def test_no_attrs(self):
#         d = self._make_one(
#             meta={'type': 'T', 'self': 'test://partial_object'}
#         )
#         self.assertEqual(d.content.a, 'a')
#         self.assertEqual(d.meta.b, 'b')

#     def test_existing_attrs(self):
#         d = self._make_one(
#             meta={'type': 'T', 'self': 'test://partial_object', 'b': 'bb'},
#             content={'a': 'aa'}
#         )
#         self.assertEqual(d.content.a, 'aa')
#         self.assertEqual(d.meta.b, 'bb')
#         self.assertEqual(d.content.x, 'x')  # Trigger rerfesh
#         self.assertEqual(d.content.a, 'a')
#         self.assertEqual(d.meta.b, 'b')

#     def test_attr_error(self):
#         d = self._make_one(
#             meta={'type': 'T', 'self': 'test://partial_object', 'b': 'bb'},
#             content={'a': 'aa'}
#         )
#         self.assertRaises(AttributeError, getattr, d.content, 'not_found')
#         self.assertRaises(AttributeError, getattr, d.meta, 'not_found')
#         self.assertRaises(AttributeError, getattr, d.meta, 'a')
#         self.assertRaises(AttributeError, getattr, d.content, 'b')
