# Cordova Hybrid App

Use the ODA Web SDK in a Cordova based native app to integrate skills or Digital Assistant.

## Requirements

* This sample requires [NodeJS](https://nodejs.org/) to install dependencies. It is compatible with latest versions of nodeJS.

* This sample requires [Apache Cordova](https://cordova.apache.org/#getstarted) to be installed in your system.
```sh
$ npm install -g cordova
```

* To build Android and iOS apps, you need to have Android Studio and Xcode installed respectively.

## Installation

At the root of the folder, run the command below to install dependencies and cordova plugins.
```sh
cordova prepare
```

Cordova will use the dependencies and declarations in package.json to install the platforms and plugins automatically.

> Note: You may observe some issues in installation of plugins for ios platform. To remedy that, you can run command to install ios platform before running the prepare command.
```sh
cordova platform add ios
cordova prepare
```

Once the platforms are added, check the requirements to see any additional installations or steps are needed to be performed.
```sh
cordova requirements
```

## Build

Once the platforms and plugins are added, you'll need to build the apps for specific platforms. To create builds for all platforms, run `cordova build`. To build for specific platform append the command with the platform name.

```sh
cordova build           # Build all platforms

cordova build android   # Build for Android

cordova build browser   # Build for Browsers

cordova build ios       # Build for iOS
```

## Run

Once the requirements are met, and builds are ready, you can run the apps.

### Android

```sh
cordova run android
```

### Web

```
cordova run browser
```

### iOS

```
cordova run ios
```

The above command will run the app in your emulator if no device is connected to your machine.

If you want to test the app on an iPhone or an iPad, you will need to use Xcode. Open `./platforms/ios` in Xcode and build from there. You will need to provide a signature to run your app on the physical devices.
