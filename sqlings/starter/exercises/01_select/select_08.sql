/*

This next one is a bit tricky, but incredibly powerful. Get ready!

Real world is messy, and in constant change. Sometimes, even columns in
databases might get deleted or added! If we try to select a column that does not
exist, the database will throw an error. So in some situations, we might want to
guard ourselves against deletions by selecting columns with a condition
that might evaluate to true (column is selected) or false (column is not
    selected)!

The task is quite simple, write a query that selects all columns that contain
the word "aircraft" in the column name from the aircraft table. There is an easy
way to do this and a more sophisticated way that will guard against future
column deletions or additions!

*/

select null;

