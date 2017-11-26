drop database if exists codely;
create database codely;
  use codely;
  create table users(
    username varchar(50) primary key,
    password varchar(50)
  );
  create table repositories(
    repo_id int auto_increment primary key,
    repo_name varchar(20),
    owner varchar(50), foreign key(owner) references users(username),
    unique(owner, repo_name)
  );
  create table commits(
    username varchar(50), foreign key(username) references users(username),
    repo_id int, foreign key(repo_id) references repositories(repo_id),
    commit_time datetime default current_timestamp
  );
  create table collaborators(
    username varchar(50), foreign key(username) references users(username),
    repo_id int, foreign key(repo_id) references repositories(repo_id),
    primary key(username, repo_id)
  );
  create table repo_tags(
    repo_id int, foreign key(repo_id) references repositories(repo_id),
    topic varchar(20),
    primary key(repo_id, topic)
  );
-- End of file --
