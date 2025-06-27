import React from 'react'
import './Footer.css'

const Footer = () => {
  return (
    <div className='mt-4 p-4 bg-[#f7f7f7] foot text-center'>
       <p className=''>Просто pet-проект по созданию временных заметок чтобы проверить/развить навыки</p>
       <p className=''>@{(new Date().getFullYear())}</p>
    </div>
  )
}

export default Footer