'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem } from "@/components/ui/command"
import { Check, ChevronsUpDown } from 'lucide-react'
import { cn } from '../../../lib/utils'

export default function PopoverSelector({ label, placeholder, selected, onChange }) {
  const [open, setOpen] = useState(false)
  const [inputValue, setInputValue] = useState("")
  const [suggestions, setSuggestions] = useState([])

  const fetchSuggestions = (input) => {
    if (!input) {
      setSuggestions([])
      return
    }
    const newSuggestions = Array.from({ length: 5 }, (_, i) => `${input} Suggestion ${i + 1}`)
    setSuggestions(newSuggestions)
  }

  const handleInputChange = (e) => {
    const input = e.target.value
    setInputValue(input)
    fetchSuggestions(input)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" className="w-[300px] justify-between">
          {selected || label}
          <ChevronsUpDown className="ml-2 h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[300px] p-0">
        <Command>
          <CommandInput placeholder={placeholder} value={inputValue} onChange={handleInputChange} />
          <CommandEmpty>No {label.toLowerCase()} found.</CommandEmpty>
          <CommandGroup>
            {suggestions.map((item) => (
              <CommandItem key={item} onSelect={() => { onChange(item); setOpen(false); setInputValue(""); setSuggestions([]) }}>
                <Check className={cn("mr-2 h-4 w-4", selected === item ? "opacity-100" : "opacity-0")} />
                {item}
              </CommandItem>
            ))}
          </CommandGroup>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
