# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Customer'
        db.create_table('romashop_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('romashop', ['Customer'])

        # Adding model 'Product'
        db.create_table('romashop_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_publish', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=70, db_index=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['romashop.Category'], null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('old_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=2, blank=True)),
            ('short_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('long_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('romashop', ['Product'])

        # Adding model 'Category'
        db.create_table('romashop_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['romashop.Category'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('romashop', ['Category'])

        # Adding model 'Picture'
        db.create_table('romashop_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['romashop.Product'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('romashop', ['Picture'])

        # Adding model 'Order'
        db.create_table('romashop_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['romashop.Customer'])),
            ('number', self.gf('django.db.models.fields.CharField')(default='0', max_length=70)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 2, 5, 14, 22, 9, 290765))),
            ('shipping_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['romashop.ShippingMethod'], null=True, blank=True)),
            ('payment_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['romashop.PaymentMethod'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('summary', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal('romashop', ['Order'])

        # Adding model 'OrderDetail'
        db.create_table('romashop_orderdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['romashop.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['romashop.Product'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('quantity', self.gf('django.db.models.fields.FloatField')()),
            ('total_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
        ))
        db.send_create_signal('romashop', ['OrderDetail'])

        # Adding model 'PaymentMethod'
        db.create_table('romashop_paymentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=2)),
            ('is_percent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('romashop', ['PaymentMethod'])

        # Adding model 'ShippingMethod'
        db.create_table('romashop_shippingmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=12, decimal_places=2)),
            ('is_percent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('romashop', ['ShippingMethod'])

        # Adding model 'Discount'
        db.create_table('romashop_discount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('is_global', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('tax', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=2)),
            ('is_percent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('romashop', ['Discount'])

        # Adding M2M table for field products on 'Discount'
        db.create_table('romashop_discount_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('discount', models.ForeignKey(orm['romashop.discount'], null=False)),
            ('product', models.ForeignKey(orm['romashop.product'], null=False))
        ))
        db.create_unique('romashop_discount_products', ['discount_id', 'product_id'])

        # Adding model 'Review'
        db.create_table('romashop_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('datetime_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 2, 5, 14, 22, 9, 294152))),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('romashop', ['Review'])

        # Adding model 'CallQuery'
        db.create_table('romashop_callquery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('datetime_added', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 2, 5, 14, 22, 9, 294869))),
            ('datetime_completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('romashop', ['CallQuery'])


    def backwards(self, orm):
        
        # Deleting model 'Customer'
        db.delete_table('romashop_customer')

        # Deleting model 'Product'
        db.delete_table('romashop_product')

        # Deleting model 'Category'
        db.delete_table('romashop_category')

        # Deleting model 'Picture'
        db.delete_table('romashop_picture')

        # Deleting model 'Order'
        db.delete_table('romashop_order')

        # Deleting model 'OrderDetail'
        db.delete_table('romashop_orderdetail')

        # Deleting model 'PaymentMethod'
        db.delete_table('romashop_paymentmethod')

        # Deleting model 'ShippingMethod'
        db.delete_table('romashop_shippingmethod')

        # Deleting model 'Discount'
        db.delete_table('romashop_discount')

        # Removing M2M table for field products on 'Discount'
        db.delete_table('romashop_discount_products')

        # Deleting model 'Review'
        db.delete_table('romashop_review')

        # Deleting model 'CallQuery'
        db.delete_table('romashop_callquery')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'romashop.callquery': {
            'Meta': {'ordering': "['-datetime_added']", 'object_name': 'CallQuery'},
            'datetime_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 5, 14, 22, 9, 294869)'}),
            'datetime_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'romashop.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['romashop.Category']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'romashop.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'romashop.discount': {
            'Meta': {'object_name': 'Discount'},
            'date_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_global': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_percent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['romashop.Product']", 'symmetrical': 'False'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'romashop.order': {
            'Meta': {'object_name': 'Order'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['romashop.Customer']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 5, 14, 22, 9, 290765)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '70'}),
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['romashop.PaymentMethod']", 'null': 'True', 'blank': 'True'}),
            'shipping_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['romashop.ShippingMethod']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'summary': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'})
        },
        'romashop.orderdetail': {
            'Meta': {'object_name': 'OrderDetail'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['romashop.Order']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['romashop.Product']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'total_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'})
        },
        'romashop.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_percent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'romashop.picture': {
            'Meta': {'object_name': 'Picture'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['romashop.Product']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'romashop.product': {
            'Meta': {'object_name': 'Product'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['romashop.Category']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_publish': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'old_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '70', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        'romashop.review': {
            'Meta': {'ordering': "['-datetime_added']", 'object_name': 'Review'},
            'datetime_added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 5, 14, 22, 9, 294152)'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'romashop.shippingmethod': {
            'Meta': {'object_name': 'ShippingMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_percent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'tax': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '12', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['romashop']
