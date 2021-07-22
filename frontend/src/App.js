import React, {useEffect, useState} from 'react'

const App = () => {
  const [timeNow, setTimeNow] = useState("")
  useEffect(() => {
    setInterval(() => {
      setTimeNow(new Date().toISOString())
    }, 1000)
  }, [])
  return (
    <div>
      <h1>Hello, World!</h1>
      <b>{timeNow}</b>
    </div>
  )
}

export default App