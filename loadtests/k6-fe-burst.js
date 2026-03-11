import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://localhost').replace(/\/$/, '');

const RAMP_UP_1 = __ENV.RAMP_UP_1 || '30s';
const RAMP_UP_1_TARGET = Number(__ENV.RAMP_UP_1_TARGET || 50);
const RAMP_UP_2 = __ENV.RAMP_UP_2 || '90s';
const RAMP_UP_2_TARGET = Number(__ENV.RAMP_UP_2_TARGET || 120);
const HOLD = __ENV.HOLD || '60s';
const RAMP_DOWN = __ENV.RAMP_DOWN || '30s';

export const options = {
  stages: [
    { duration: RAMP_UP_1, target: RAMP_UP_1_TARGET },
    { duration: RAMP_UP_2, target: RAMP_UP_2_TARGET },
    { duration: HOLD, target: RAMP_UP_2_TARGET },
    { duration: RAMP_DOWN, target: 0 },
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<1200'],
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/`);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'html response': (r) => (r.headers['Content-Type'] || '').includes('text/html'),
  });
}
