============================
Simple Blogging Application
============================

**How to install code:**

1.git clone https://github.com/shitalp/blog
  
2.cd blog    
  
3.sudo python3 setup.py install

**How to run code:**
  
1.blog --help will list help and commands available

2.blog post add "title" "content" will add a new blog a new blog post with title and content.

3.blog post post list will list all blog posts

4.blog post search "keyword" will list all blog posts where “keyword” is found in title and/or content.

5.blog category add "category-name" create a new category

6.blog category list list all categories

7.blog category assign <post-id> <cat-id> assign category to post

8.blog post add "title" "content" --category "cat-name" will add a new blog a new blog post 


**How to run test cases**

1.cd tests

2.wget https://raw.githubusercontent.com/lehmannro/assert.sh/master/assert.sh

3.bash tests.sh
