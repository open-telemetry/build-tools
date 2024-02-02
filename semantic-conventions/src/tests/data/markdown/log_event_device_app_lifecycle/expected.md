# Test

<!-- semconv device.app.lifecycle -->
The event name MUST be `device.app.lifecycle`.

| Body Field  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `android.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. [1] | `created` | Recommended |
| `ios.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. [2] | `active` | Recommended |


**[1]:** The Android lifecycle states are defined in [Activity lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS identifiers` are derived.

**[2]:** The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902), and from which the `OS terminology` column values are derived.

`android.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `created` | Any time before Activity.onResume() or, if the app has no Activity, Context.startService() has been called in the app for the first time. |
| `background` | Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state. |
| `foreground` | Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states. |

`ios.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `active` | The app has become `active`. Associated with UIKit notification `applicationDidBecomeActive`. |
| `inactive` | The app is now `inactive`. Associated with UIKit notification `applicationWillResignActive`. |
| `background` | The app is now in the background. This value is associated with UIKit notification `applicationDidEnterBackground`. |
| `foreground` | The app is now in the foreground. This value is associated with UIKit notification `applicationWillEnterForeground`. |
| `terminate` | The app is about to terminate. Associated with UIKit notification `applicationWillTerminate`. |
<!-- endsemconv -->
