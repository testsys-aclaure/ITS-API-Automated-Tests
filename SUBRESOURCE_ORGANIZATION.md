# Sub-Resource Pipeline Organization Summary
**Total Pipelines Created:** 43
**Total Endpoints Covered:** 84

## Pipeline Structure
- `form-validation.yml` -> `tests/form/` (4 endpoints)
- `test-validation.yml` -> `tests/test/` (4 endpoints)
- `timezone-validation.yml` -> `tests/timezone/` (1 endpoints)
- `user-validation.yml` -> `tests/user/` (2 endpoints)
- `channel_institutions-validation.yml` -> `tests/channel_institutions/` (2 endpoints)
- `event-validation.yml` -> `tests/event/` (4 endpoints)
- `event_class-validation.yml` -> `tests/event_class/` (4 endpoints)
- `event_class_examinees-validation.yml` -> `tests/event_class_examinees/` (3 endpoints)
- `event_authorizations-validation.yml` -> `tests/event_authorizations/` (1 endpoints)
- `event_examinee-validation.yml` -> `tests/event_examinee/` (1 endpoints)
- `examinee-validation.yml` -> `tests/examinee/` (3 endpoints)
- `examinee_audit-validation.yml` -> `tests/examinee_audit/` (1 endpoints)
- `examinee_events-validation.yml` -> `tests/examinee_events/` (1 endpoints)
- `examinee_longitudinal_segment_detail-validation.yml` -> `tests/examinee_longitudinal_segment_detail/` (1 endpoints)
- `examinee_longitudinal_segments-validation.yml` -> `tests/examinee_longitudinal_segments/` (1 endpoints)
- `examinee_record-validation.yml` -> `tests/examinee_record/` (1 endpoints)
- `form_definition-validation.yml` -> `tests/form_definition/` (2 endpoints)
- `form_reports-validation.yml` -> `tests/form_reports/` (1 endpoints)
- `form_res_files-validation.yml` -> `tests/form_res_files/` (1 endpoints)
- `inventory-validation.yml` -> `tests/inventory/` (1 endpoints)
- `iw_tool-validation.yml` -> `tests/iw_tool/` (4 endpoints)
- `longitudinal_group_examinees-validation.yml` -> `tests/longitudinal_group_examinees/` (4 endpoints)
- `message_history-validation.yml` -> `tests/message_history/` (1 endpoints)
- `order-validation.yml` -> `tests/order/` (3 endpoints)
- `package_forms-validation.yml` -> `tests/package_forms/` (1 endpoints)
- `registration-validation.yml` -> `tests/registration/` (4 endpoints)
- `remote_admin_urls-validation.yml` -> `tests/remote_admin_urls/` (1 endpoints)
- `remote_examinee_data-validation.yml` -> `tests/remote_examinee_data/` (1 endpoints)
- `remote_practice_checks-validation.yml` -> `tests/remote_practice_checks/` (1 endpoints)
- `remote_session_data-validation.yml` -> `tests/remote_session_data/` (1 endpoints)
- `remote_sessions-validation.yml` -> `tests/remote_sessions/` (4 endpoints)
- `remote_system_checks-validation.yml` -> `tests/remote_system_checks/` (1 endpoints)
- `result-validation.yml` -> `tests/result/` (3 endpoints)
- `result_identifier-validation.yml` -> `tests/result_identifier/` (1 endpoints)
- `sabbatical-validation.yml` -> `tests/sabbatical/` (1 endpoints)
- `secure_browser_errors-validation.yml` -> `tests/secure_browser_errors/` (1 endpoints)
- `secure_browser_tokens-validation.yml` -> `tests/secure_browser_tokens/` (1 endpoints)
- `session-validation.yml` -> `tests/session/` (4 endpoints)
- `signalr_domain-validation.yml` -> `tests/signalr_domain/` (1 endpoints)
- `start_test-validation.yml` -> `tests/start_test/` (2 endpoints)
- `test_forms-validation.yml` -> `tests/test_forms/` (1 endpoints)
- `test_pretest_references-validation.yml` -> `tests/test_pretest_references/` (2 endpoints)
- `user_access-validation.yml` -> `tests/user_access/` (2 endpoints)

## Next Steps
1. Create Azure Pipeline YAML files for each sub-resource
2. Configure path-based triggers in Azure DevOps
3. Test minimal viable payloads for POST endpoints
4. Set up deployment validation workflows