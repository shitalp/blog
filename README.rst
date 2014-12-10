1.first download blog file from https://github.com/shitalp/blog
  and then unzip it and install it by using following command.
  sudo python3 setup.py install
2.Edit file by using: 
   vim /etc/blog/blog.cfg
3.run code:
   blog
4.how to run test caes:
  1.assert "./test.py post add 1 1 " "post_content : 1\npost_title: 1\nPost Added"
  2.assert_raises "./test.py post list" 0
  3.assert "./test.py post add 1 1 -C 1" "post_content : 1\npost_title: 1\nPost Added\nCatogry assigned to post"
  4.assert_raises "./test.py post search 1" 0
  5.assert "./test.py category add 1  " "name: 1"
  6.assert_raises "./test.py category list" 0
  7.assert_raises "./test.py category assign 1" 0


