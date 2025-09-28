/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { CrmKanbanModel } from "@crm_ts/views/crm_ts_kanban/crm_ts_kanban_model";
import { CrmKanbanArchParser } from "@crm_ts/views/crm_ts_kanban/crm_ts_kanban_arch_parser";
import { CrmKanbanRenderer } from "@crm_ts/views/crm_ts_kanban/crm_ts_kanban_renderer";

export const crmKanbanView = {
    ...kanbanView,
    ArchParser: CrmKanbanArchParser,
    // Makes it easier to patch
    Controller: class extends kanbanView.Controller {
        get progressBarAggregateFields() {
            const res = super.progressBarAggregateFields;
            const progressAttributes = this.props.archInfo.progressAttributes;
            if (progressAttributes && progressAttributes.recurring_revenue_sum_field) {
                res.push(progressAttributes.recurring_revenue_sum_field);
            }
            return res;
        }
    },
    Model: CrmKanbanModel,
    Renderer: CrmKanbanRenderer,
};

registry.category("views").add("crm_ts_kanban", crmKanbanView);
