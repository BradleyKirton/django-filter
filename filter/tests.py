__test__ = {"filterset": """
>>> from django import forms
>>> from django.core.management import call_command
>>> import filter
>>> from filter import FilterSet
>>> from filter.widgets import LinkWidget
>>> from filter.models import User, Comment, Book, STATUS_CHOICES

>>> call_command('loaddata', 'test_data', verbosity=0)

>>> class F(FilterSet):
...     class Meta:
...         model = User

>>> F.base_filters.keys()
['username', 'first_name', 'last_name', 'status', 'is_active', 'favorite_books']

>>> class F(FilterSet):
...     class Meta:
...         model = User
...         exclude = ['is_active']

>>> F.base_filters.keys()
['username', 'first_name', 'last_name', 'status', 'favorite_books']

>>> class F(FilterSet):
...     class Meta:
...         model = User
...         fields = ['status']

>>> f = F({'status': '1'}, queryset=User.objects.all())
>>> f.qs
[<User: alex>]
>>> print f.form
<tr><th><label for="id_status">Status:</label></th><td><select name="status" id="id_status">
<option value="0">Regular</option>
<option value="1" selected="selected">Admin</option>
</select></td></tr>

>>> class F(FilterSet):
...     status = filter.ChoiceFilter(widget=forms.RadioSelect, choices=STATUS_CHOICES)
...     class Meta:
...         model = User
...         fields = ['status']

>>> f = F(queryset=User.objects.all())
>>> print f.form
<tr><th><label for="id_status_0">Status:</label></th><td><ul>
<li><label for="id_status_0"><input type="radio" id="id_status_0" value="0" name="status" /> Regular</label></li>
<li><label for="id_status_1"><input type="radio" id="id_status_1" value="1" name="status" /> Admin</label></li>
</ul></td></tr>


>>> class F(FilterSet):
...     class Meta:
...         model = User
...         fields = ['username']

>>> F.base_filters.keys()
['username']

>>> f = F(queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>, <User: jacob>]
>>> f = F({'username': 'alex'}, queryset=User.objects.all())
>>> f.qs
[<User: alex>]
>>> print f.form
<tr><th><label for="id_username">Username:</label></th><td><input type="text" name="username" value="alex" id="id_username" /></td></tr>

>>> class F(FilterSet):
...     username = filter.CharFilter(action=lambda qs, value: qs.filter(**{'username__startswith': value}))
...     class Meta:
...         model = User
...         fields = ['username']

>>> f = F({'username': 'a'}, queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>]

>>> class F(FilterSet):
...     status = filter.MultipleChoiceFilter(choices=STATUS_CHOICES)
...     class Meta:
...         model = User
...         fields = ['status']

>>> f = F(queryset=User.objects.all())
>>> print f.form
<tr><th><label for="id_status">Status:</label></th><td><select multiple="multiple" name="status" id="id_status">
<option value="0">Regular</option>
<option value="1">Admin</option>
</select></td></tr>
>>> f.qs
[<User: alex>, <User: aaron>, <User: jacob>]
>>> f = F({'status': ['0']}, queryset=User.objects.all())
>>> f.qs
[<User: aaron>, <User: jacob>]
>>> f = F({'status': ['0', '1']}, queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>, <User: jacob>]

>>> class F(FilterSet):
...     class Meta:
...         model = Comment
...         fields = ['date']

>>> f = F({'date': '01/30/09'}, queryset=Comment.objects.all())
>>> f.qs
[<Comment: alex said super awesome!>]

>>> class F(FilterSet):
...     class Meta:
...         model = Comment
...         fields = ['author']

>>> f = F({'author': '2'}, queryset=Comment.objects.all())
>>> f.qs
[<Comment: aaron said psycadelic!>]

>>> class F(FilterSet):
...     class Meta:
...         model = User
...         fields = ['favorite_books']
>>> f = F(queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>, <User: jacob>]

>>> f = F({'favorite_books': ['1']}, queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>]
>>> f = F({'favorite_books': ['1', '3']}, queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>]
>>> f = F({'favorite_books': ['2']}, queryset=User.objects.all())
>>> f.qs
[<User: alex>]

>>> class F(FilterSet):
...     class Meta:
...         model = User
...         fields = ['name', 'status']
...         order_by = ['status']
>>> f = F({'o': 'status'}, queryset=User.objects.all())
>>> f.qs
[<User: aaron>, <User: jacob>, <User: alex>]
>>> print f.form
<tr><th><label for="id_status">Status:</label></th><td><select name="status" id="id_status">
<option value="0">Regular</option>
<option value="1">Admin</option>
</select></td></tr>
<tr><th><label for="id_o">Ordering:</label></th><td><select name="o" id="id_o">
<option value="status" selected="selected">Status</option>
</select></td></tr>
>>> class F(FilterSet):
...     class Meta:
...         model = User
...         fields = ['username', 'status']
...         order_by = True
>>> f = F({'o': 'username'}, queryset=User.objects.all())
>>> f.qs
[<User: aaron>, <User: alex>, <User: jacob>]
>>> print f.form
<tr><th><label for="id_username">Username:</label></th><td><input type="text" name="username" id="id_username" /></td></tr>
<tr><th><label for="id_status">Status:</label></th><td><select name="status" id="id_status">
<option value="0">Regular</option>
<option value="1">Admin</option>
</select></td></tr>
<tr><th><label for="id_o">Ordering:</label></th><td><select name="o" id="id_o">
<option value="username" selected="selected">Username</option>
<option value="status">Status</option>
</select></td></tr>

>>> class F(FilterSet):
...     price = filter.NumberFilter(lookup_type='lt')
...     class Meta:
...         model = Book
...         fields = ['price']

>>> f = F({'price': 15}, queryset=Book.objects.all())
>>> f.qs
[<Book: Ender's Game>]

>>> class F(FilterSet):
...     class Meta:
...         model = User
...         fields = ['is_active']

'2' and '3' are how the field expects the data from the browser
>>> f = F({'is_active': '2'}, queryset=User.objects.all())
>>> f.qs
[<User: jacob>]
>>> f = F({'is_active': '3'}, queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>]
>>> f = F({'is_active': '1'}, queryset=User.objects.all())
>>> f.qs
[<User: alex>, <User: aaron>, <User: jacob>]
>>> class F(FilterSet):
...     average_rating = filter.NumberFilter(lookup_type='gt')
...     class Meta:
...         model = Book
...         fields = ['average_rating']

>>> f = F({'average_rating': '4.5'}, queryset=Book.objects.all())
>>> f.qs
[<Book: Ender's Game>, <Book: Rainbox Six>]

>>> class F(FilterSet):
...     class Meta:
...         model = Comment
...         fields = ['time']

>>> f = F({'time': '12:55'}, queryset=Comment.objects.all())
>>> f.qs
[<Comment: jacob said funky fresh!>]

>>> class F(FilterSet):
...     price = filter.RangeFilter()
...     class Meta:
...         model = Book
...         fields = ['price']
>>> f = F(queryset=Book.objects.all())
>>> print f.form
<tr><th><label for="id_price_0">Price:</label></th><td><input type="text" name="price_0" id="id_price_0" />-<input type="text" name="price_1" id="id_price_1" /></td></tr>
>>> f.qs
[<Book: Ender's Game>, <Book: Rainbox Six>, <Book: Snowcrash>]
>>> f = F({'price_0': '5', 'price_1': '15'}, queryset=Book.objects.all())
>>> f.qs
[<Book: Ender's Game>, <Book: Rainbox Six>]

>>> class F(FilterSet):
...     price = filter.NumberFilter(lookup_type=None)
...     class Meta:
...         model = Book
...         fields = ['price']
>>> f = F(queryset=Book.objects.all())
>>> print f.form
<tr><th><label for="id_price_0">Price:</label></th><td><input type="text" name="price_0" id="id_price_0" /><select name="price_1" id="id_price_1">
<option value="contains">contains</option>
<option value="day">day</option>
<option value="endswith">endswith</option>
<option value="exact">exact</option>
<option value="gt">gt</option>
<option value="gte">gte</option>
<option value="icontains">icontains</option>
<option value="iendswith">iendswith</option>
<option value="iexact">iexact</option>
<option value="in">in</option>
<option value="iregex">iregex</option>
<option value="isnull">isnull</option>
<option value="istartswith">istartswith</option>
<option value="lt">lt</option>
<option value="lte">lte</option>
<option value="month">month</option>
<option value="range">range</option>
<option value="regex">regex</option>
<option value="search">search</option>
<option value="startswith">startswith</option>
<option value="week_day">week_day</option>
<option value="year">year</option>
</select></td></tr>
>>> class F(FilterSet):
...     price = filter.NumberFilter(lookup_type=['lt', 'gt'])
...     class Meta:
...         model = Book
...         fields = ['price']
>>> f = F(queryset=Book.objects.all())
>>> print f.form
<tr><th><label for="id_price_0">Price:</label></th><td><input type="text" name="price_0" id="id_price_0" /><select name="price_1" id="id_price_1">
<option value="gt">gt</option>
<option value="lt">lt</option>
</select></td></tr>
>>> f = F({'price_0': '15', 'price_1': 'lt'}, queryset=Book.objects.all())
>>> f.qs
[<Book: Ender's Game>]
>>> f= F({'price_0': '15', 'price_1': 'lt'})
>>> f.qs
[<Book: Ender's Game>]
>>> class F(FilterSet):
...     status = filter.ChoiceFilter(widget=LinkWidget, choices=STATUS_CHOICES)
...     class Meta:
...         model = User
...         fields = ['status']
>>> f = F()
>>> f.qs
[<User: alex>, <User: aaron>, <User: jacob>]
>>> print f.form
<tr><th><label for="id_status">Status:</label></th><td><ul id="id_status">
<li><a href="?status=0">Regular</a></li>
<li><a href="?status=1">Admin</a></li>
</ul></td></tr>
>>> f = F({'status': '1'})
>>> f.qs
[<User: alex>]
>>> print f.form
<tr><th><label for="id_status">Status:</label></th><td><ul id="id_status">
<li><a href="?status=0">Regular</a></li>
<li><a href="?status=1">Admin</a></li>
</ul></td></tr>

"""}

