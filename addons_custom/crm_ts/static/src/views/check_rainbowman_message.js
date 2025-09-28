/** @odoo-module **/

export async function checkRainbowmanMessage(orm, effect, recordId) {
    const message = await orm.call("crm_ts.lead", "get_rainbowman_message", [[recordId]]);
    if (message) {
        effect.add({
            message,
            type: "rainbow_man",
        });
    }
}
