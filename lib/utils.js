// src/lib/utils.js

// `cn` is a utility function for conditionally joining class names.
export function cn(...classes) {
    return classes.filter(Boolean).join(' ')
  }
  