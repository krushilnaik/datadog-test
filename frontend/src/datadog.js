import { datadogRum } from "@datadog/browser-rum";
import { reactPlugin } from "@datadog/browser-rum-react";

datadogRum.init({
  applicationId: process.env.REACT_APP_DD_APP_ID,
  clientToken: process.env.REACT_APP_DD_CLIENT_TOKEN,
  site: "datadoghq.com",
  service: "frontend",
  env: process.env.DD_ENV || "local",
  version: "1.0.0",
  sessionSampleRate: 100,
  sessionReplaySampleRate: 20,
  defaultPrivacyLevel: "mask-user-input",
  plugins: [reactPlugin],
});

// datadogRum.startSessionReplayRecording();

export default datadogRum;
