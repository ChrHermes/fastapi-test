<template>
    <Dialog v-model:open="open">
      <DialogTrigger as-child>
        <Button>
          Logeintrag hinzufügen
        </Button>
      </DialogTrigger>
  
      <DialogContent class="max-w-sm">
        <DialogHeader>
          <DialogTitle>Neuen Logeintrag hinzufügen</DialogTitle>
        </DialogHeader>
  
        <div class="space-y-2">
          <Input
            ref="inputRef"
            v-model="newMessage"
            placeholder="Nachricht eingeben"
            @keydown.enter.prevent="submit"
          />
  
          <Select v-model="newLevel">
            <SelectTrigger>
              <SelectValue placeholder="Level auswählen" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="INFO">INFO</SelectItem>
              <SelectItem value="USER">USER</SelectItem>
              <SelectItem value="DEBUG">DEBUG</SelectItem>
              <SelectItem value="ERROR">ERROR</SelectItem>
            </SelectContent>
          </Select>
        </div>
  
        <div class="flex justify-end gap-2 pt-4">
          <DialogClose as-child>
            <Button variant="ghost">Abbrechen</Button>
          </DialogClose>
          <Button
            :disabled="!newMessage || !newLevel"
            @click="submit"
          >
            Hinzufügen
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  </template>
  
  <script setup>
  import { ref, watch, nextTick } from 'vue'
  import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogClose
  } from '@/components/ui/dialog'
  import { Button } from '@/components/ui/button'
  import { Input } from '@/components/ui/input'
  import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
  } from '@/components/ui/select'
  
  const emit = defineEmits(['submit'])
  
  const open = ref(false)
  const newMessage = ref('')
  const newLevel = ref('USER')
  const inputRef = ref(null)
  
  function submit() {
    if (!newMessage.value || !newLevel.value) return
  
    const entry = {
      timestamp: new Date().toISOString(), // wird vom Parent formatiert
      level: newLevel.value,
      message: newMessage.value,
    }
  
    emit('submit', entry)
  
    // Reset + schließen
    newMessage.value = ''
    newLevel.value = 'USER'
    open.value = false
  }
  
  // 🔍 Auto-Fokus sobald geöffnet
  watch(open, (val) => {
    if (val) {
      nextTick(() => {
        inputRef.value?.focus()
      })
    }
  })
  </script>
  