define(`PLATFORM_SUFFIX',translit(defn(`PLATFORM'),`A-Z',`a-z'))dnl
define(`PLATFORM_RESOURCES',dnl
ifelse(defn(`PLATFORM'),`Xeon',,dnl
#          resources:
#            limits:
#              gpu.intel.com/i915: 1
          securityContext:
            privileged: true
            runAsUser: 0
))dnl
define(`PLATFORM_NODE_SELECTOR',dnl
      affinity:
          nodeAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
                - matchExpressions:
                  - key: "xeone3-zone"
                    operator: `ifelse(defn(`PLATFORM'),`XeonE3',ifelse($1,`XeonE3',`In',`NotIn'),`NotIn')'
                    values:
                       - "xeone3"
)dnl
