#!/usr/bin/env bash
# Helper script to manually trigger a Sentinel investigation against sentinel-sim.
# Use this when the CI/CD pipeline isn't set up or you want to test from a
# developer laptop.
#
# Usage:
#   ./scripts/trigger-incident.sh crashloop    # CrashLoopBackOff
#   ./scripts/trigger-incident.sh oom          # OOMKilled
#   ./scripts/trigger-incident.sh bad-config   # ConfigMap mismatch
#   ./scripts/trigger-incident.sh bad-deploy   # ImagePullBackOff
set -e

INCIDENT_TYPE="${1:-crashloop}"
NAMESPACE="${NAMESPACE:-sim}"
SENTINEL_NS="${SENTINEL_NS:-sentinel}"

case "$INCIDENT_TYPE" in
  crashloop|oom|bad-config|bad-deploy)
    ;;
  *)
    echo "Usage: $0 {crashloop|oom|bad-config|bad-deploy}"
    exit 1
    ;;
esac

INCIDENT_NAME="sim-${INCIDENT_TYPE}-$(date +%s)"
echo "Creating SentinelIncident: $INCIDENT_NAME"

cat <<EOF | kubectl apply -f -
apiVersion: sentinel.io/v1alpha1
kind: SentinelIncident
metadata:
  name: $INCIDENT_NAME
  namespace: $SENTINEL_NS
spec:
  service: sentinel-sim
  namespace: $NAMESPACE
  reason: "Manual trigger of $INCIDENT_TYPE incident for testing"
  trigger: manual
  repo: karimzakzoukz/sentinel-sim
EOF

echo ""
echo "✓ Incident created. Sentinel's CRD watcher will pick it up within 10s."
echo ""
echo "Watch Sentinel's investigation:"
echo "  kubectl -n $SENTINEL_NS logs -f deploy/sentinel-core"
echo ""
echo "Check incident status:"
echo "  kubectl -n $SENTINEL_NS get sentinelincidents.sentinel.io $INCIDENT_NAME -o yaml"
