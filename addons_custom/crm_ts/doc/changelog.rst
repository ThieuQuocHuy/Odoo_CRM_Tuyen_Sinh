.. _changelog:

Changelog
=========

`trunk (saas-2)`
----------------

- Stage/state update

  - ``crm_ts.lead``: removed ``state`` field. Added ``date_last_stage_update`` field
    holding last stage_id modification. Updated reports.
  - ``crm_ts.case.stage``: removed ``state`` field.

- ``crm_ts``, ``crm_ts_claim``: removed inheritance from ``base_stage`` class. Missing
  methods have been added into ``crm_ts`` and ``crm_ts_claim``. Also removed inheritance
  in ``crm_ts_helpdesk`` because it uses states, not stages.
