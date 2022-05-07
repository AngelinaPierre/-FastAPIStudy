import React, {useState} from "react";
import FormInput from '../FormInput/FormInput'
import PopupModal from '../Modal/PopupModal'
import Recipe from '../Recipe'

const RecipeTable = () => {

    const [recipeInfoModal, setRecipeInfoModal] = useState(false)
    return(
        <>
            <div className='sections-list'>
                <Recipe />
            </div>
            {recipeInfoModal && <PopupModal
						modalTitle={"Recipe Info"}
						onCloseBtnPress={() => {
							setRecipeInfoModal(false);
						}}
					>
						<div className="mt-4 text-left">
							<form className="mt-5">
								<FormInput
									disabled
									type={"text"}
									name={"label"}
									label={"Label"}
									value={recipeInfoModal?.label}
								/>
								<FormInput
									disabled
									type={"text"}
									name={"url"}
									label={"Url"}
									value={recipeInfoModal?.url}
								/>
								<FormInput
									disabled
									type={"text"}
									name={"source"}
									label={"Source"}
									value={recipeInfoModal?.source}
								/>
							</form>
						</div>
					</PopupModal>
                }
        </>
    )
}

export default RecipeTable;