from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

# Create your tests here.
class FirstTestCase(TestCase):
    def setUp(self):
        print('setup called')
        
    def test_user(self):
       user = User.objects.create_user(
           username='gfdgfgf', email='testcategory@gmail.com'
       )
       user.set_password('pass12345')
       user.save()
       self.assertEqual(str(user), 'gfdgfgf')
       
    def test_level(self):
           level = Level.objects.create(
               name='medium'
           )
           level.save()
           self.assertEqual(str(level), 'medium')

    def test_Author(self):
        author = Author.objects.create(
            
            name='Alif', about_author="hello"
        )
        author.save()
        self.assertEqual(str(author), 'Alif')

    def test_language(self):
        lang = Language.objects.create(

            language='Hindi'
        )
        lang.save()
        self.assertEqual(str(lang), 'Hindi')

    def test_category(self):
        category = Categories.objects.create(

            icon='', name="Laravel"
        )
        category.save()
        self.assertEqual(str(category), 'Laravel')

    def test_newcategorycourse(self):
        category = Categories.objects.create(

            icon='', name="Laravel"
        )
        category.save()
        author = Author.objects.create(

            name='Alif', about_author="hello"
        )
        author.save()
        level = Level.objects.create(
            name='medium'
        )
        level.save()
        lang = Language.objects.create(

            language='Hindi'
        )
        lang.save()
        course=Course.objects.create(
            title='New Course',author=author,category=category,level=level,language=lang,description='new desc',price= 200, discount=30,Deadline ='Always'
            
        )
        course.save()
        self.assertEqual(str(course),'New Course')
        
    def test_wyl(self):
            category = Categories.objects.create(

                icon='', name="Laravel"
            )
            category.save()
            author = Author.objects.create(

                name='Alif', about_author="hello"
            )
            author.save()
            level = Level.objects.create(
                name='medium'
            )
            level.save()
            lang = Language.objects.create(

                language='Hindi'
            )
            lang.save()
            course = Course.objects.create(
                title='New Course', author=author, category=category, level=level, language=lang, description='new desc', price=200, discount=30, Deadline='Always'

            )
            course.save()
            wyl = What_you_learn.objects.create(
                course=course,points='Mewmew'
            )
            wyl.save()
            self.assertEqual(str(wyl), 'Mewmew')

    def test_req(self):
        category = Categories.objects.create(

            icon='', name="Laravel"
        )
        category.save()
        author = Author.objects.create(

            name='Alif', about_author="hello"
        )
        author.save()
        level = Level.objects.create(
            name='medium'
        )
        level.save()
        lang = Language.objects.create(

            language='Hindi'
        )
        lang.save()
        course = Course.objects.create(
            title='New Course', author=author, category=category, level=level, language=lang, description='new desc', price=200, discount=30, Deadline='Always'

        )
        course.save()
        req = Requirements.objects.create(
            course=course, points='cat'
        )
        req.save()
        self.assertEqual(str(req), 'cat')
    
    def test_vid(self):
        category = Categories.objects.create(

            icon='', name="Laravel"
        )
        category.save()
        author = Author.objects.create(

            name='Alif', about_author="hello"
        )
        author.save()
        level = Level.objects.create(
            name='medium'
        )
        level.save()
        lang = Language.objects.create(

            language='Hindi'
        )
        lang.save()
        course = Course.objects.create(
            title='New Course', author=author, category=category, level=level, language=lang, description='new desc', price=200, discount=30, Deadline='Always'

        )
        course.save()
        lesson = Lesson.objects.create(
            course=course, name='newlesson'
        )
        lesson.save()
        vid= Video.objects.create(
            course=course, lesson=lesson, title='newvid',youtube_id='hfchf45'
        )
        vid.save()
        self.assertEqual(str(vid),'newvid')
        
       
       