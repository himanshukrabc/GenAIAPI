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

  class ChatActionChain extends ActionChain {

    /**
     * @param {Object} context
     */
    async run(context) {
      const { $page, $flow, $application, $constants, $variables } = context;

      if ($variables.query == null) {
        await Actions.fireNotificationEvent(context, {
          displayMode: 'persist',
        });
      }
      else {

        $variables.chats = [
  ...$variables.chats,
  {
    textdata: $variables.query,
    srdata: null,
    docdata: null,
    'is_user': true,
citations: null
  },
];
        $variables.past_Query = $variables.query;

        await Actions.resetVariables(context, {
          variables: [
            '$page.variables.query',
          ],
        });
        const response = await Actions.callRest(context, {
          endpoint: 'getSol/post',
          body: {
            query: $page.variables.past_Query,
          },
          responseBodyFormat: 'json',
          responseType: 'resp',
        });

        $variables.data = response.body.data;
        $variables.chats = [
  ...$variables.chats,
  {
    textdata: response.body.data,
    srdata: response.body.sr_response,
    docdata: response.body.doc_response,
    'is_user': false,
citations: response.body.citations
  },
];

      }


    }
  }

  return ChatActionChain;
});
