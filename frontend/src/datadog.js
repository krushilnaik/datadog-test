import { datadogRum } from "@datadog/browser-rum";

datadogRum.init({
  applicationId: process.env.REACT_APP_DD_APP_ID,
  clientToken: process.env.REACT_APP_DD_CLIENT_TOKEN,
  site: "datadoghq.com",
  service: "frontend",
  env: "dev",
  version: "1.0.0",
  allowedTracingUrls: [
    {
      match: "http://backend:8000",
      propagatorTypes: ["datadog"],
    },
  ],
});

datadogRum.startSessionReplayRecording();

export default datadogRum;
