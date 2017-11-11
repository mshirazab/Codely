create database if not exists codely;
  use codely;
  drop table if exists users;
  create table users(
    username varchar(50) primary key,
    password varchar(50)
  );
  drop table if exists repositories;
  create table repositories(
    repo_id int primary key,
    repo_name varchar(20),
    owner varchar(50), foreign key(owner) references user(username),
    unique(username, repo_name)
  );
  drop table if exists commits;
  create table commits(
    username varchar(50), foreign key(username) references user(username),
    repo_id int, foreign key(repo_id) references repository(repo_id),
    commit_time datetime,
  );
  drop table if exists collaborators;
  create table collaborators(
    username varchar(50), foreign key(username) references user(username),
    repo_id int, foreign key(repo_id) references repository(repo_id),
    primary key(username, repo_id)
  );
  drop table if exists repo_tags;
  create table repo_tags(
    repo_id int, foreign key(repo_id) references repository(repo_id),
    topic varchar(20),
    foreign key(repo_id, topic)
  );
