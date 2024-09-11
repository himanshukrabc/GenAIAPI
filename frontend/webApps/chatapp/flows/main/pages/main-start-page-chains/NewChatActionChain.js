define([
  'vb/action/actionChain',
  'vb/action/actions',
  'vb/action/actionUtils',
], (
  ActionChain,
  Actions,
  ActionUtils
) => {
  'use strict';

  class NewChatActionChain extends ActionChain {

    /**
     * @param {Object} context
     */
    async run(context) {
      const { $page, $flow, $application, $constants, $variables } = context;

      await Actions.resetVariables(context, {
        variables: [
    '$page.variables.chats',
    '$page.variables.query',
  ],
      });

      const response = await Actions.callRest(context, {
        endpoint: 'resetContext/getReset',
        responseBodyFormat: 'json',
        responseType: 'resetResp',
      });
    }
  }

  return NewChatActionChain;
});
