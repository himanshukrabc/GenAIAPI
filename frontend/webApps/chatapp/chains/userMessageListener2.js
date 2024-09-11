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

  class userMessageListener2 extends ActionChain {

    /**
     * @param {Object} context
     * @param {Object} params
     * @param {{oldValue:getPostsId,value:getPostsId}} params.event
     */
    async run(context, { event }) {
      const { $application, $constants, $variables } = context;
    }
  }

  return userMessageListener2;
});
