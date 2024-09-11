/**
  Copyright (c) 2015, 2021, Oracle and/or its affiliates.
  Licensed under The Universal Permissive License (UPL), Version 1.0
  as shown at https://oss.oracle.com/licenses/upl/

*/
define(['ojs/ojcomposite', 'text!./card-message-view.html', './card-message-viewModel', 'text!./component.json', 'css!./card-message-styles.css'],
  function(Composite, view, viewModel, metadata) {
    Composite.register('card-message', {
      view: view,
      viewModel: viewModel,
      metadata: JSON.parse(metadata)
    });
  }
);