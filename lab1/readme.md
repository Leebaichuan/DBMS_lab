# DBMS lab1 介绍
## PB18111679 范文


### 功能说明
#### 本次实验的 `sql` 脚本都放在了本目录下，其中每个文件的功能如下：

* `readme.md` 本文件，作为实验介绍
* `db-lab01.pdf` 实验1的要求
* `my_init.sql` 用于第一题中的创建基本表和插入我自己编的测试数据
* `integriy.sql` 用于第二题中测试 `sql` 的三类完整性
* `test.sql` 助教给的测试数据
* `query.sql` 用于第三题的查询
* `change_ID.sql` 用于第四题的实现对图书 `ID` 的修改的存储过程
* `change_status.sql` 用于第五题的实现对图书 `status` 的检查的存储过程
* `status_trigger.sql` 用于第六题的实现对图书 `status` 修改的触发器

### 运行测试

* 首先，运行 `my_init.sql` 文件初始化数据库，再运行 `integriy.sql` 文件进行完整性测试。（实际上，`integriy.sql`中的三条验证用户完整性的语句都会由于不满足完整性而报错，需要分开来运行）

* 然后，运行 `test.sql` 加载测试数据，并依次运行 `query.sql`, `change_ID.sql`, `change_status.sql`, `status_trigger.sql` 来检查实验结果。
