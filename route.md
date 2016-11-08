## 路由

1. @app.route('/'(*#路由地址*), methods=['GET','POST'] (*#请求方法*)]

   ```python
   @app.route('/', methods=['GET'])
   def home():
       return 'hello world'
   ```

* 固定路由地址结尾带`'/'`和不带的区别：

  1. 带`'/'`可以自动重定向不带`'/'`的url访问，比如：

       `@app.route('/user/', methods=['GET'])`就可以重定向`http://localhos/user`到`http://localhost/user/`从而保证同一个页面不会有两个路由的地址

  2. 不带`'/'`的路由地址不能解析带`'/'`的url访问，比如：

     `@app.route('/user', methods=['GET'])`不能解析`http://localhost/user/`这个url请求，只会返回404 not found错误

* 动态路由地址

  1. 路由地址可以用`<>`包围表示为一个动态的路由地址

     ```python
     @app.route('/hello/<username>')
     def show_user_profile(username):
         return 'goodmorning %s' % username
     ```

  2. 动态路由地址也可以通过转换器进行筛选过滤

     * 其规则为`<converter:variable_name>`


     * converter有三种类型分别为：int、float、path(和默认的相似，但它能接受斜线)

       ```python
       @app.route('/check/<int:id>')
       def show_post(id):
           # if the id is enable or unable
           return 'success(or fialer) %d' % post_id
       ```

       如果访问了带有转换器筛选的路由地址，动态的内容不符合转换器的规则则会返回404 not found

       比如访问上面的路由地址，但是动态的部分不是int类型：`http://localhost/check/str`

