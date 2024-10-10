📝 Sqlings
================

Welcome to Sqlings! This project contains small exercises that you can use to
learn SQL interactively. Sqlings is heavily influenced by
[Rustlings](https://github.com/rust-lang/rustlings), which is a similar
type of application for learning the Rust programming language.


💬 Installation
------------

Prerequisites:

* A modern terminal emulator, like Wezterm, Kitty, Alacritty or Windows Terminal
* Python 3.12 (it may or may not work on other python versions)

Grab the latest wheel from the release-page and install that with pip or any
other package manager.

Ensure you have Sqlings properly installed by running the `sqlings` command from
the command line.

If you encounter problems, please raise an issue and describe your problem!


💬 Getting started
------------

When you have Sqlings properly installed, create a new project by running
`sqlings new project_name` in your terminal. Replace "project_name" with
whatever name you prefer. Then open your project in your code editor of choice,
and in a separate terminal window run `sqlings start`. The output in your
terminal will tell you which exercise you should solve next and give you a
description of the task (and a more or less helpful error message).

Sqlings comes bundled with an existing DuckDB database located in your project
that contains a few aviation-related tables that are used in the exercises. In
order to explore the data, you can open the DuckDB database in a SQL editor
(e.g. [Harlequin](https://github.com/tconbeer/harlequin)), but make sure to open
the database file in **read-only mode**, otherwise it will prohibit Sqlings from
reading the data in the database which will cause an error.

Sqlings will analyze your progress in real time, just make sure you press 'n'
when you are ready to proceed to the next exercise.

Good luck and have fun!
