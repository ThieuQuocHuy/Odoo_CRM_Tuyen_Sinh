/** @odoo-module **/

import { crmKanbanView } from "@crm_ts/views/crm_ts_kanban/crm_ts_kanban_view";

export class ForecastKanbanController extends crmKanbanView.Controller {
    isQuickCreateField(field) {
        return super.isQuickCreateField(...arguments) || (field && field.name === "date_deadline");
    }
}
