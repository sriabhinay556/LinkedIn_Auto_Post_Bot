'use client'

import { useState } from 'react'

export function Popover({ children, open, onOpenChange }) {
  const handleToggle = () => onOpenChange(!open)

  return (
    <div className="relative">
      {React.Children.map(children, (child) =>
        child.type === PopoverTrigger ? React.cloneElement(child, { onToggle: handleToggle }) : child
      )}
    </div>
  )
}

export function PopoverTrigger({ children, onToggle }) {
  return <div onClick={onToggle}>{children}</div>
}

export function PopoverContent({ children, className }) {
  return (
    <div className={`absolute z-10 bg-white border border-gray-200 rounded-md shadow-lg p-4 ${className}`}>
      {children}
    </div>
  )
}
