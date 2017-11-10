create database if not exists codely;
  use codely;
  drop table if exists user;
  create table user(
    username varchar(50) primary key,
    password varchar(50)
  );
