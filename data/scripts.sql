DELETE FROM comment WHERE body = '[removed]';

--ejq72yv, b7abt0

SELECT * FROM comment WHERE id = 'ejq72yv';
SELECT * FROM comment WHERE parent_id = 'ejq72yv';

-- Find comments
with recursive tr(parent_id, id, level) as (
      select c.parent_id, c.id, 1 as level
      from comment c union all
      select c1.parent_id, tr.id, tr.level + 1
      from comment c1 join
           tr
           on c1.id = tr.parent_id
    )
select tr.id, maxlevel
from (select tr.*,
             max(level) over (partition by parent_id) as maxlevel
      from tr
) tr
where level = maxlevel AND maxlevel > 9;

-- Show count of all comments and posts
SELECT 'Posts' as Type, COUNT(*) FROM post UNION SELECT 'Comments' as Type, COUNT(*) FROM comment;

SELECT COUNT(*) FROM comment c WHERE c.inserted > '2019-04-06';
SELECT COUNT(*) FROM post p WHERE p.inserted > '2019-04-06';

DELETE FROM comment c WHERE c.inserted > '2019-04-06';
DELETE FROM post p WHERE p.inserted > '2019-04-06';