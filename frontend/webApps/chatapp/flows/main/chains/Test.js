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

  class Test extends ActionChain {

    /**
     * @param {Object} context
     */
    async run(context) {
      const { $flow, $application, $constants, $variables } = context;

      const response = await Actions.callRest(context, {
        endpoint: 'demo_SN/postObjects',
      });
    }
  }

  return Test;
});
