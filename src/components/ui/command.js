'use client'

import { useState } from 'react'

export function Command({ children }) {
  return <div className="command-container">{children}</div>
}

export function CommandInput({ placeholder, value, onChange }) {
  return (
    <input
      type="text"
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className="w-full p-2 border-b outline-none"
    />
  )
}

export function CommandEmpty({ children }) {
  return <div className="p-2 text-gray-500 text-center">{children}</div>
}

export function CommandGroup({ children }) {
  return <div className="p-2">{children}</div>
}

export function CommandItem({ children, onSelect }) {
  return (
    <div onClick={onSelect} className="cursor-pointer p-2 hover:bg-gray-100 rounded">
      {children}
    </div>
  )
}
