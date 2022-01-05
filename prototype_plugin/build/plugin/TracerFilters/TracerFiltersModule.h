
#ifndef TRACERFILTERS_EXPORT_H
#define TRACERFILTERS_EXPORT_H

#ifdef TRACERFILTERS_STATIC_DEFINE
#  define TRACERFILTERS_EXPORT
#  define TRACERFILTERS_NO_EXPORT
#else
#  ifndef TRACERFILTERS_EXPORT
#    ifdef TracerFilters_EXPORTS
        /* We are building this library */
#      define TRACERFILTERS_EXPORT __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define TRACERFILTERS_EXPORT __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef TRACERFILTERS_NO_EXPORT
#    define TRACERFILTERS_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef TRACERFILTERS_DEPRECATED
#  define TRACERFILTERS_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef TRACERFILTERS_DEPRECATED_EXPORT
#  define TRACERFILTERS_DEPRECATED_EXPORT TRACERFILTERS_EXPORT TRACERFILTERS_DEPRECATED
#endif

#ifndef TRACERFILTERS_DEPRECATED_NO_EXPORT
#  define TRACERFILTERS_DEPRECATED_NO_EXPORT TRACERFILTERS_NO_EXPORT TRACERFILTERS_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef TRACERFILTERS_NO_DEPRECATED
#    define TRACERFILTERS_NO_DEPRECATED
#  endif
#endif

#endif /* TRACERFILTERS_EXPORT_H */
