\set aid random(1, 100000 * :scale)
\set bid random(1, 1 * :scale)
\set tid random(1, 10 * :scale)
\set delta random(-5000, 5000)
BEGIN;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
SELECT abalance FROM pgbench_accounts WHERE aid = :aid;
UPDATE pgbench_accounts SET abalance = abalance + :delta WHERE aid = :aid;
END;