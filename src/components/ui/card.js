'use client'

export function Card({ children, className }) {
  return <div className={`rounded-lg shadow-md ${className}`}>{children}</div>
}

export function CardContent({ children, className }) {
  return <div className={`p-4 ${className}`}>{children}</div>
}

export function CardFooter({ children, className }) {
  return <div className={`p-4 border-t ${className}`}>{children}</div>
}
